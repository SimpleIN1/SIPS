import {EType} from "@/enums/EType";
import {LatLngExpression} from "leaflet";

export interface ISettlement{
    name: string,
    population: number,
    type: EType,
    poly: LatLngExpression[],
    longitude: number,
    latitude: number
}