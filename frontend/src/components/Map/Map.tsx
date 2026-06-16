import "./Map.scss";
import { MapContainer, TileLayer } from "react-leaflet";
import { LatLngExpression, LatLngLiteral } from "leaflet";
import type { MouseEvent } from "react";

import { Legend } from "@/components/Settings/Legend/Legend";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import Coords from "@/components/Map/Coords/Coords";
import Settings from "@/components/Settings";
import Ruler from "@/components/Map/Ruler/Ruler";
import { addRulerMarker, addRulerMarkerPos } from "@/store/ruler/ruler-slice";
import Cursor from "@/components/Cursor/Cursor";
import Regions from "@/components/Map/Regions/Regions";
import NatureReserves from "@/components/Map/NatureReserves/NatureReserves";
import RulerMarkers from "@/components/Map/RulerMarkers/RulerMarkers";
import Settlements from "@/components/Map/Settlements/Settlements";
import { Loading } from "@/components/main/Loading/Loading";
import { TileService } from "@/components/TileService/TileService";

const CENTR: LatLngExpression = [54.84643545576913, 83.05183410644533];

const Map = () => {
  const dispatch = useAppDispatch();

  const layer = useAppSelector((state) => state.map.layer);
  const isRulerActive = useAppSelector((state) => state.ruler.isRulerActive);
  const mousePos: LatLngLiteral = useAppSelector((state) => state.cursor.mousePos);
  const isCursorActive = useAppSelector((state) => state.cursor.isActive);

  const isRegions = useAppSelector((state) => state.map.isRegions);
  const isNatureReserves = useAppSelector((state) => state.map.isNatureReserves);
  const isSettlements = useAppSelector((state) => state.map.isSettlements);
  const isLoading = useAppSelector((state) => state.map.isLoading);

  const satelliteState = useAppSelector((state) => state.tile.satellite);
  const compositeState = useAppSelector((state) => state.tile.composite);
  const date = useAppSelector((state) => state.tile.dateTime.nondotdate);
  const time = useAppSelector((state) => state.tile.dateTime.time);

  const addMarker = (event: MouseEvent<HTMLDivElement>) => {
    if (!isRulerActive) return;

    const isNotBottomPanel = event.clientY < window.innerHeight - 68;
    const isNotRightPanel = event.clientX < window.innerWidth - 116;

    if (isNotBottomPanel || isNotRightPanel) {
      dispatch(addRulerMarker({ position: mousePos, title: "" }));
      dispatch(addRulerMarkerPos([mousePos.lat, mousePos.lng]));
    }
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="mapPage" onClick={isRulerActive ? addMarker : undefined}>
      <MapContainer
        className="leafletMap"
        center={CENTR}
        zoom={3}
        minZoom={3}
        maxZoom={13}
        scrollWheelZoom={true}
        doubleClickZoom={false}
        maxBounds={[
            [-110, -170],
            [100, 200],
        ]}
        >
        <TileLayer
          key={layer}
          url={layer}
          opacity={1}
          zIndex={1}
        />

        {satelliteState && compositeState && time && date && <TileService />}

        {isRegions && <Regions />}
        {isNatureReserves && <NatureReserves />}
        {isSettlements && <Settlements />}

        <RulerMarkers />

        <Coords />
        <Settings />
        {compositeState && <Legend composite={compositeState} />}

        <Ruler />

        {isCursorActive && <Cursor />}
      </MapContainer>
    </div>
  );
};

export default Map;