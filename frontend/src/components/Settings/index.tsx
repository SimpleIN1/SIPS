import { useEffect, useRef, useState } from "react";
import type { MouseEvent, WheelEvent } from "react";
import { DomEvent } from "leaflet";
import s from "./Settings.module.scss";

import { useAppSelector } from "@/hooks/hook";

import LayerSwitch from "./LayerSwitch/LayerSwitch";
import AdditionalInformation from "./AdditionalInformation/AdditionalInformation";
import Satelite from "./Satelite";
import Composites from "./Composites";

import Calendar from "@/components/Calendar";
import TimeLine from "@/components/Calendar/TimeLine/TimeLine";
import DownloadSelectedProduct from "@/components/Settings/DownloadSelectedProduct/DownloadSelectedProduct";

const Settings = () => {
  const panelRef = useRef<HTMLElement | null>(null);

  const satellite = useAppSelector((state) => state.tile.satellite);
  const dotDate = useAppSelector((state) => state.tile.dateTime.dotdate);
  const time = useAppSelector((state) => state.tile.dateTime.time);

  const isDateEnabled = Boolean(satellite);
  const isTimeEnabled = Boolean(satellite && dotDate);
  const isCompositeEnabled = Boolean(satellite && dotDate && time);

  const [isPanelOpen, setIsPanelOpen] = useState(true);

  const [layerOpen, setLayerOpen] = useState(true);
  const [additionalOpen, setAdditionalOpen] = useState(true);
  const [satelliteOpen, setSatelliteOpen] = useState(true);
  const [dateOpen, setDateOpen] = useState(true);
  const [compositeOpen, setCompositeOpen] = useState(true);

  useEffect(() => {
    if (!isPanelOpen || !panelRef.current) {
      return;
    }

    DomEvent.disableScrollPropagation(panelRef.current);
    DomEvent.disableClickPropagation(panelRef.current);
  }, [isPanelOpen]);

  const stopMapEvents = (
    event: MouseEvent<HTMLElement> | WheelEvent<HTMLElement>
  ) => {
    event.stopPropagation();
  };

  if (!isPanelOpen) {
    return (
      <div
        className={s.hiddenPanel}
        onWheel={stopMapEvents}
        onClick={stopMapEvents}
        onMouseDown={stopMapEvents}
        onDoubleClick={stopMapEvents}
      >
        <button
          type="button"
          className={s.openPanelButton}
          onClick={() => setIsPanelOpen(true)}
        >
          Фильтры ›
        </button>
      </div>
    );
  }

  return (
    <aside
      ref={panelRef}
      className={s.sidebar}
      onWheel={stopMapEvents}
      onWheelCapture={stopMapEvents}
      onClick={stopMapEvents}
      onMouseDown={stopMapEvents}
      onDoubleClick={stopMapEvents}
    >
      <div className={s.topLine}>
        <h2 className={s.title}>Фильтры</h2>

        <button
          type="button"
          className={s.hideButton}
          onClick={() => setIsPanelOpen(false)}
          title="Скрыть панель"
        >
          ‹
        </button>
      </div>

      <div
        className={s.scroll}
        onWheel={stopMapEvents}
        onWheelCapture={stopMapEvents}
      >
        <div className={s.filterBlock}>
          <div
            className={s.filterHeader}
            onClick={() => setLayerOpen(!layerOpen)}
          >
            <span>Выбор слоя</span>
            <span className={s.filterArrow}>{layerOpen ? "▾" : "▸"}</span>
          </div>

          {layerOpen && (
            <div className={s.filterContent}>
              <LayerSwitch />
            </div>
          )}
        </div>

        <div className={s.filterBlock}>
          <div
            className={s.filterHeader}
            onClick={() => setAdditionalOpen(!additionalOpen)}
          >
            <span>Дополнительные данные</span>
            <span className={s.filterArrow}>
              {additionalOpen ? "▾" : "▸"}
            </span>
          </div>

          {additionalOpen && (
            <div className={s.filterContent}>
              <AdditionalInformation />
            </div>
          )}
        </div>

        <div className={s.filterBlock}>
          <div
            className={s.filterHeader}
            onClick={() => setSatelliteOpen(!satelliteOpen)}
          >
            <span>Спутниковые снимки</span>
            <span className={s.filterArrow}>
              {satelliteOpen ? "▾" : "▸"}
            </span>
          </div>

          {satelliteOpen && (
            <div className={s.filterContent}>
              <Satelite />
            </div>
          )}
        </div>

        <div className={s.filterBlock}>
          <div
            className={s.filterHeader}
            onClick={() => setDateOpen(!dateOpen)}
          >
            <span>Дата и время</span>
            <span className={s.filterArrow}>{dateOpen ? "▾" : "▸"}</span>
          </div>

          {dateOpen && (
            <div className={s.filterContent}>
              <div className={s.calendarWrapper}>
                <Calendar disabled={!isDateEnabled} />
              </div>

              <TimeLine disabled={!isTimeEnabled} />

              <DownloadSelectedProduct />
            </div>
          )}
        </div>

        <div className={s.filterBlock}>
          <div
            className={s.filterHeader}
            onClick={() => setCompositeOpen(!compositeOpen)}
          >
            <span>Композиты VIIRS</span>
            <span className={s.filterArrow}>
              {compositeOpen ? "▾" : "▸"}
            </span>
          </div>

          {compositeOpen && (
            <div className={s.filterContent}>
              <Composites disabled={!isCompositeEnabled} />
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Settings;