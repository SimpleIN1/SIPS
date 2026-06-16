import React from 'react';
import {useAppSelector} from "@/hooks/hook";
import {Polygon, Popup} from "react-leaflet";
import {IRegion} from "@/interfaces/IRegion";

export default React.memo(function Regions () {
    const purpleOptions = { color: 'red' }
    const regions:IRegion[] = useAppSelector(state => state.map).polygons.regions
    return (
        <>
            {regions.map((region, index) => (
                <Polygon key = {index} pathOptions={purpleOptions} positions={region.polygons}><Popup>{region.name}</Popup></Polygon>
            ))}
        </>
    );
})
