import {LatLngLiteral} from "leaflet";

export interface CursorState{
    mousePos: LatLngLiteral,
    cursorPosition:{
        x: number,
        y: number,
    }
    isActive: boolean
}