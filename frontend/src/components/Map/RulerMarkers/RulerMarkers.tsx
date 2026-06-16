import React from 'react';
import {Marker, Polyline, Tooltip} from "react-leaflet";
import {icons} from "@/data/icons";
import {RulerCalculations} from "@/utils/RulerCalculations";
import {IMarker} from "@/interfaces/IMarker";
import {useAppSelector} from "@/hooks/hook";
import {LatLngExpression} from "leaflet";
import {IRulerObj} from "@/interfaces/IRulerObj";

const RulerMarkers = () => {
    const purpleOptions = { color: 'red' }
    const rulerMarkers:IMarker[] = useAppSelector(state => state.ruler).rulerMarkers
    const rulerMarkersPos:LatLngExpression[] = useAppSelector(state => state.ruler).rulerMarkersPos
    return (
        <>
            {rulerMarkers.map((marker, index) => (
                <Marker key = {index} position = {marker.position} icon = {icons().rulerIcon} />
            ))}

            {RulerCalculations.iterateLatLng(rulerMarkersPos).map((marker:IRulerObj, index: number) => (
                <Marker key = {index} position = {marker.pos} icon = {icons().emptyIcon}>
                    <Tooltip permanent>{marker.title}</Tooltip>
                </Marker>
            ))}

            <Polyline dashArray="5 10" pathOptions={purpleOptions} positions={rulerMarkersPos} />
        </>
    );
};

export default RulerMarkers;