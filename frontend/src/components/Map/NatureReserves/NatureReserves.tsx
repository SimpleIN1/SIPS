import React from 'react';
import {useAppSelector} from "@/hooks/hook";
import {Polygon} from "react-leaflet";
import {LatLngExpression} from "leaflet";

export default React.memo(function Regions () {
    const greenOptions = { color: 'green' }
    const natureReserves:LatLngExpression[][] = useAppSelector(state => state.map).polygons.natureReserves
    return (
        <>
            {natureReserves.map((region, index) => (
                <Polygon key = {index} pathOptions={greenOptions} positions={region} />
            ))}
        </>
    );
})
