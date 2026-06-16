import React from 'react';
import s from './Coords.module.scss'
import {useMap, useMapEvents} from "react-leaflet";
import {useAppDispatch, useAppSelector} from "@/hooks/hook";
import {setMousePos} from "@/store/cursor/cursor-slice";
import {LatLngLiteral} from "leaflet";
import {disableMapDragging, enableMapDragging} from "@/utils/mapdragging";
import {convertCoords} from "@/utils/coords";

const Coords = () => {

    const mousePos: LatLngLiteral = useAppSelector(state => state.cursor).mousePos
    const dispatch = useAppDispatch()



    const map = useMap()


    const _coords = useMapEvents({

        mousemove: (event) => {
            dispatch(setMousePos({lat: event.latlng.lat, lng: event.latlng.lng}));
        },
    });

    const handleMouseDown = () => {
        disableMapDragging(map)
    }
    const handleMouseUp = () => {
        enableMapDragging(map)
    }

    return (
        <div
            className={s.coords}
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
        >
            <div>{convertCoords(mousePos.lat)} {mousePos.lat < 0 ? 'ю': 'с'}.ш</div>
            <div>{convertCoords(mousePos.lng)} {mousePos.lng < 0 ? 'з': 'в'}.д</div>
        </div>
    );
};

export default Coords;