import {IPolygons} from "@/interfaces/IPolygons";
import {IBorder} from "@/interfaces/IBorder";

export interface MapState{
    layer: string,
    polygons: IPolygons,
    borders: IBorder[],
    isLoading: boolean,
    isRegions: boolean,
    isNatureReserves: boolean,
    isSettlements: boolean
}