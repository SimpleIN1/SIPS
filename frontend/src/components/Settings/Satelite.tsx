import FormControlLabel from "@mui/material/FormControlLabel";
import Switch from "@mui/material/Switch";
import s from "./Settings.module.scss";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { setSatellite } from "@/store/tile/tile-slice";
import { fetchDates } from "@/store/tile/tile-actions";
import { ESatellite } from "@/enums/ESatellite";
import { ISatelliteResponse } from "@/interfaces/ISatelliteResponse";

const Satelite = () => {
  const dispatch = useAppDispatch();

  const selectedSatellite = useAppSelector((state) => state.tile.satellite);

  const satellitesFromStore: ISatelliteResponse[] =
    useAppSelector((state) => state.tile.satellites) || [];

  const satellites: ISatelliteResponse[] =
    satellitesFromStore.length > 0
      ? satellitesFromStore
      : [
          { id: 1, name: "Suomi NPP", tag: ESatellite.SUOMI_NPP },
          { id: 2, name: "NOAA-20", tag: ESatellite.NOAA_20 },
        ];

  const isSatelliteDisabled = (satelliteTag: string) => {
    return satelliteTag === ESatellite.NOAA_20;
  };

  const satelliteHandleChange = (value: string) => {
    if (isSatelliteDisabled(value)) {
      return;
    }

    dispatch(setSatellite(value as ESatellite));
    dispatch(fetchDates(value));
  };

  return (
    <div className={s.satelliteList}>
      {satellites.map((satellite) => {
        const disabled = isSatelliteDisabled(satellite.tag);

        return (
          <FormControlLabel
            key={satellite.id}
            control={
              <Switch
                checked={selectedSatellite === satellite.tag}
                disabled={disabled}
                onChange={() => satelliteHandleChange(satellite.tag)}
              />
            }
            label={
              disabled
                ? `${satellite.name} — данные отсутствуют`
                : satellite.name
            }
          />
        );
      })}
    </div>
  );
};

export default Satelite;