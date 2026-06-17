from pathlib import Path
import logging
import os.path
import pickle
from datetime import datetime, timedelta

from geoalchemy2.shape import from_shape

from api import conf
from api.celery.app import celery_app
from api.common.code_generator import generate_sequence
from api.common.composite_image import CompositeCutService, CompositeTaskContainer
from api.common.compsite_search import geocoords_to_polygon
from api.common.download_link import DownloadLinkService, make_link
from api.common.email.email_sender import SendLinksEmail
from api.common.geotiff_cut_polygon import cut_polygon
from api.common.user_file_composite import UserFileCompositeService
from api.db.models import UserFileCompositeModel, DownloadLinkModel
from api.db.requests import CompositeDataDataBaseQuery


@celery_app.task()
def remove_expired_urls():
    logging.info("Perform removing expiration files")
    ufc_service = UserFileCompositeService()
    ufc_service.delete_expiration_files()

    logging.info("Perform deleting download link")
    dl_service = DownloadLinkService()
    dl_service.delete_link()


@celery_app.task
def cut_tiff_images_by_points(byte_stream):
    logging.info("Start cut images")

    cddbq = CompositeDataDataBaseQuery()

    ctc_item: CompositeTaskContainer = pickle.loads(byte_stream)

    datetimes = [item.datetime for item in ctc_item.images]
    composites = [item.composite for item in ctc_item.images]
    satellites = [item.satellite for item in ctc_item.images]

    ccs_service = CompositeCutService()
    composite_files = ccs_service.get_composites(datetimes, composites, satellites)

    if not composite_files:
        logging.info("composite_files not found")
        return

    unicue_sequence = generate_sequence()
    dirname = f"{conf.PATH_SAFE_CUTTING_IMAGE}/{unicue_sequence}"
    Path(dirname).mkdir(parents=True, exist_ok=True)

    tokens = []
    cutting_filenames = []

    for item in composite_files:
        filename = os.path.split(item.filename)[1]
        cutting_filename = f"{os.path.splitext(filename)[0]}-cutting.tif"
        path = f"{dirname}/{cutting_filename}"

        cutting_filenames.append(cutting_filename)

        cut_polygon(
            path_src=item.filename,
            path_dst=path,
            points=ctc_item.points
        )

        polygon = geocoords_to_polygon(ctc_item.points)

        try:
            ufc_item = UserFileCompositeModel(
                user_id=ctc_item.user_id,
                file_composite_id=item.id,
                filename=path,
                polygon=from_shape(polygon, srid=4326),
                datetime_expiration=datetime.now() + timedelta(days=conf.DAYS_STORED),
                datetime_created=datetime.now()
            )
            cddbq.insert_data(ufc_item, flush=True)

            logging.info(f"UserFileCompositeModel is added {ufc_item.id}")

            token = generate_sequence()
            tokens.append(token)
            datetime_now = datetime.now()
            dl_item = DownloadLinkModel(
                token=token,
                file_composite_id=None,
                user_file_composite_id=ufc_item.id,
                user_id=ctc_item.user_id,
                datetime_expiration=datetime_now + timedelta(days=conf.DAYS_STORED),
                datetime_created=datetime_now
            )
            cddbq.insert_data(dl_item, flush=True)
            logging.info(f"DownloadLinkModel is added {dl_item.id}")
            cddbq.session.commit()
        except Exception as e:
            cddbq.session.rollback()
            logging.error(f"Session rollback {e}")
            break
    else:
        recipient = ctc_item.email
        links = [make_link(token, is_add_resource=True) for token in tokens]
        SendLinksEmail().send_message(recipient=recipient, links=links, link_names=cutting_filenames)
