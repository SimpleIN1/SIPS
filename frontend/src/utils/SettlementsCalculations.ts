import {LatLngBounds, LatLngExpression} from "leaflet";
import {EType} from "@/enums/EType";


export class SettlementsCalculations{
    static isCoordinateInsideBounds(coordinate: LatLngExpression, bounds: LatLngBounds, type:EType): boolean {
        if (type === EType.CITY){
            return true
        }
        const lat = coordinate[0]
        const lng = coordinate[1]

        return lat >= bounds.getSouthWest().lat &&
            lat <= bounds.getNorthEast().lat &&
            lng >= bounds.getSouthWest().lng &&
            lng <= bounds.getNorthEast().lng;
    }

    static getTypeArray(zoom: number): EType[] {
        // я пытался по умному
        switch (zoom){
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
            case 6:
            case 7:{
                return [EType.CITY]
            }
            case 8:
            case 9:{
                return [EType.CITY, EType.TOWN]
            }
            default:{
                return [EType.CITY, EType.TOWN, EType.VILLAGE]
            }
        }
    }
    static swapLatAndLng(array: LatLngExpression[]): LatLngExpression[] {
        const newArray: LatLngExpression[] = [];
        for (let i = 0; i < array.length; i++) {
            newArray.push([array[i][1], array[i][0]]);
        }
        return newArray;
    }


}