import {Map} from "leaflet";


export const disableMapDragging = (map: Map) => {
    map.dragging.disable();
}

export const enableMapDragging = (map: Map) => {
    map.dragging.enable()
}