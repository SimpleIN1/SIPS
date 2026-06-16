import {LatLngExpression} from "leaflet";

export interface IRegion{
    name: string,
    polygons: LatLngExpression[]
}