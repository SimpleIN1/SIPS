import { Switch } from "@mui/material";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { fetchRegions } from "@/store/map/map-actions";
import { setAdditionalLayerVisible } from "@/store/map/map-slice";
import { EUrls } from "@/enums/EUrls";
import s from "../Settings.module.scss";

const AdditionalInformation = () => {
  const dispatch = useAppDispatch();

  const borders = useAppSelector((state) => state.map.borders);
  const polygons = useAppSelector((state) => state.map.polygons);

  const isRegions = useAppSelector((state) => state.map.isRegions);
  const isNatureReserves = useAppSelector(
    (state) => state.map.isNatureReserves
  );
  const isSettlements = useAppSelector((state) => state.map.isSettlements);

  const getIsVisible = (url: string) => {
    switch (url) {
      case EUrls.REGIONS_URL:
        return isRegions;

      case EUrls.NATURE_RESERVES_URL:
        return isNatureReserves;

      case EUrls.SETTLEMENTS_URL:
        return isSettlements;

      default:
        return false;
    }
  };

  const getIsLoaded = (url: string) => {
    switch (url) {
      case EUrls.REGIONS_URL:
        return polygons.regions.length > 0;

      case EUrls.NATURE_RESERVES_URL:
        return polygons.natureReserves.length > 0;

      case EUrls.SETTLEMENTS_URL:
        return polygons.settlements.length > 0;

      default:
        return false;
    }
  };

  const handleChange = (url: EUrls | string, checked: boolean) => {
    dispatch(
      setAdditionalLayerVisible({
        url,
        isVisible: checked,
      })
    );

    if (checked && !getIsLoaded(url)) {
      dispatch(fetchRegions(url));
    }
  };

  return (
    <div className={s.additionalLayers}>
      {borders.map((item) => (
        <div key={item.url} className={s.additionalLayerRow}>
          <span className={s.additionalLayerName}>{item.name}</span>

          <Switch
            checked={getIsVisible(item.url)}
            onChange={(event) => handleChange(item.url, event.target.checked)}
            size="medium"
            sx={{
              transform: "scale(1.08)",
              "& .MuiSwitch-switchBase.Mui-checked": {
                color: "#2563eb",
              },
              "& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track": {
                backgroundColor: "#2563eb",
              },
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default AdditionalInformation;