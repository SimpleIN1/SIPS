import { useState } from "react";
import s from "./LeftBar.module.scss";
import { FaSearch } from "react-icons/fa";
import { IoMdDownload } from "react-icons/io";
import { CatalogItem } from "@/components/Pages/Catalog/LeftBar/CatalogItem/CatalogItem";
import { CiSettings } from "react-icons/ci";
import { CiCalendar } from "react-icons/ci";
import { SettingsLeft } from "./settings/SettingsLeft";
import { CalendarLeft } from "./calendar/CalendarLeft";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { convert } from "@/utils/calendar";
import { IImage } from "@/interfaces/IImage";
import { fetchCatalogItems } from "@/store/catalog/catalog-actions";
import { IImages } from "@/interfaces/IImages";
import TileService from "@/service/tile-service";

export const LeftBar = () => {
  const dispatch = useAppDispatch();

  const satellite: string = useAppSelector((state) => state.catalog).sattelite;
  const composite: string = useAppSelector((state) => state.catalog).composite;
  const startDay: string = useAppSelector((state) => state.catalog).start_day;
  const endDay: string = useAppSelector((state) => state.catalog).end_day;
  const dates: string[] = useAppSelector((state) => state.tile).dotdates;
  const imagesObj: IImages = useAppSelector((state) => state.catalog).imagesObj;

  const [selectAllChecked, setSelectAllChecked] = useState<boolean>(false);
  const [isSetOpen, setIsSetOpen] = useState<boolean>(false);
  const [isCaleOpen, setIsCaleOpen] = useState<boolean>(false);

  const handleSelectAllChecked = () => {
    setSelectAllChecked((value) => !value);
  };

  const handleOpenSett = () => {
    setIsSetOpen((value) => !value);
  };

  const handleOpenCale = () => {
    setIsCaleOpen((value) => !value);
  };

  const handleSearch = async () => {
    if (!satellite || !composite || !startDay || !endDay) {
      return;
    }

    const filteredDates = dates.filter((date) => {
      const convertedDateValue = convert(date).value;

      return (
        convertedDateValue >= convert(startDay).value &&
        convertedDateValue <= convert(endDay).value
      );
    });

    const timesByDates = await Promise.all(
      filteredDates.map(async (date) => {
        const response = await TileService.getTimes(satellite, date);
        return response.map((time) => `${date} ${time.label}`);
      })
    );

    const images: IImage[] = [];

    timesByDates.flat().forEach((datetime) => {
      images.push({
        datetime,
        composite,
        satellite,
      });
    });

    await dispatch(fetchCatalogItems(images));
  };

  return (
    <div className={s.leftbar}>
      <div className={s.btns}>
        <button type="button" onClick={handleOpenSett}>
          <CiSettings className={s.headerbtn} />
        </button>

        <button type="button" onClick={handleOpenCale}>
          <CiCalendar className={s.headerbtn} />
        </button>

        <button type="button" className={s.searchbtn} onClick={handleSearch}>
          Поиск
          <FaSearch />
        </button>
      </div>

      {isSetOpen && <SettingsLeft />}
      {isCaleOpen && <CalendarLeft />}

      <div className={s.setttab}>
        {satellite && `${satellite} | `}
        {composite && `${composite} | `}
        {startDay && endDay && `${startDay} - ${endDay}`}
      </div>

      <div className={s.btnstab}>
        <button type="button" className={s.sortbtn}>
          сортировать
        </button>

        <div className={s.choseallbtn} onClick={handleSelectAllChecked}>
          <span>выбрать все</span>
          <input type="checkbox" checked={selectAllChecked} readOnly />
        </div>

        <button type="button" className={s.downloadbtn}>
          <IoMdDownload />
        </button>
      </div>

      <div className={s.catalogitems}>
        {imagesObj.images.map((catalogitem) => (
          <CatalogItem key={catalogitem.uid} catalogitem={catalogitem} />
        ))}
      </div>
    </div>
  );
};