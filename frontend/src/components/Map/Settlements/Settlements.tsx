import React, {useEffect, useState} from 'react';
import {Marker, Polygon, Popup, useMap} from "react-leaflet";
import {useAppSelector} from "@/hooks/hook";
import {icons} from "@/data/icons";
import {SettlementsCalculations} from "@/utils/SettlementsCalculations";
import {ISettlement} from "@/interfaces/ISettlement";
import {LatLngBounds} from "leaflet";


export default React.memo(function Settlements(){

    const blueOptions = { color: 'blue' }
    const lightBlueOptions = {color : '#00a2ff'}
    const settlements:ISettlement[] = useAppSelector(state => state.map).polygons.settlements

    const map = useMap()
    const [bounds, setBounds] = useState<LatLngBounds>(new LatLngBounds([-110, -170], [100, 200]))
    const [zoom, setZoom] = useState<number>(4)

    useEffect(() => {
        const handleZoomEnd = () => {
            setZoom(map.getZoom())
            setBounds(map.getBounds())

        };
        const handleMoveEnd = () => {
            setBounds(map.getBounds())
        };
        map.on("zoomend", handleZoomEnd);
        map.on("moveend", handleMoveEnd);

        return () => {
            map.off("zoomend", handleZoomEnd);
            map.off("moveend", handleMoveEnd);
        };
    }, [map]);



    //cities, towns, villages

    return (
        <>
            {settlements.map((settlement:ISettlement, index) => (
                SettlementsCalculations.getTypeArray(zoom).includes(settlement.type)
                && SettlementsCalculations.isCoordinateInsideBounds([settlement.latitude, settlement.longitude], bounds, settlement.type)
                && ((zoom > 9 && settlement.poly !== null) ?
                    <Polygon key = {index} pathOptions={settlement.population > 50000 ? blueOptions : lightBlueOptions} positions={SettlementsCalculations.swapLatAndLng(settlement.poly)}><Popup>{settlement.population}</Popup></Polygon>
                :
                    <Marker icon = {icons().settlementIcon} key = {index} position = {[settlement.latitude, settlement.longitude]}><Popup>{settlement.name}</Popup></Marker>
                )
            ))}
        </>
    );
})
