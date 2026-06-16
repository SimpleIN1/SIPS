import {IMarker} from "@/interfaces/IMarker";
import {LatLngExpression} from "leaflet";

export interface RulerState{
    isRulerActive: boolean,
    rulerMarkers: IMarker[],
    rulerMarkersPos: LatLngExpression[],
}