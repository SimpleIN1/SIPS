import {IRegion} from "@/interfaces/IRegion";
import {LatLngExpression} from "leaflet";
import {ISettlement} from "@/interfaces/ISettlement";

export interface IPolygons{
    regions: IRegion[],
    natureReserves: LatLngExpression[][],
    settlements: ISettlement[],
}