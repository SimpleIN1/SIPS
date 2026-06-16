import React, {useEffect} from 'react';
import './../../Map/Map.scss'
import s from './Catalog.module.scss'
import Map from "@/components/Map/Map";
import {LeftBar} from "@/components/Pages/Catalog/LeftBar/LeftBar";
import Header from "@/components/Header";
import { MapContainer, TileLayer, FeatureGroup, Circle  } from 'react-leaflet';
import { LatLngExpression } from 'leaflet';
import { EditControl } from 'react-leaflet-draw';
import { checkAuth } from '@/store/user/user-actions';
import { useAppDispatch } from '@/hooks/hook';



const CENTR:LatLngExpression = [54.84643545576913, 83.05183410644533];



export const Catalog = () => {
    const dispatch = useAppDispatch();


    return (
        <div className={s.catalogcontainer}>
            <Header/>
                <div className={s.catalog}>
                    <LeftBar/>
                    <MapContainer
                                center={CENTR}
                                maxZoom={13}
                                zoom={4}
                                minZoom={3}
                                scrollWheelZoom={true}
                                maxBounds={[[-110, -170], [100, 200]]}
                                doubleClickZoom={false}
                            >
                                <TileLayer 
                                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' 
                                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" 
                                />
                            <FeatureGroup>
                                <EditControl
                                position='topright'
                                draw={{
                                    marker:false,
                                    circlemarker: false,
                                    polyline: false
                                }}
                                />
                                <Circle center={[51.51, -0.06]} radius={200} />
                            </FeatureGroup>
                    
                    </MapContainer>
                </div>
        </div>
    );
}
