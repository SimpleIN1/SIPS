import { TileLayer } from "react-leaflet";
import { useAppSelector } from "@/hooks/hook";
import { buildTileUrl } from "@/utils/tileUrl";

export const TileService = () => {
  const satellite = useAppSelector((state) => state.tile.satellite);
  const composite = useAppSelector((state) => state.tile.composite);
  const date = useAppSelector((state) => state.tile.dateTime.nondotdate);
  const time = useAppSelector((state) => state.tile.dateTime.time);

  if (!satellite || !composite || !date || !time) {
    return null;
  }

  const tileUrl = buildTileUrl(satellite, date, time, composite);

  return (
    <TileLayer
      key={`${satellite}-${date}-${time}-${composite}`}
      url={tileUrl}
      opacity={0.75}
      zIndex={10}
      maxNativeZoom={3}
      maxZoom={13}
    />
  );
};
