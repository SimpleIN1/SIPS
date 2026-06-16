import {LatLng, LatLngExpression} from "leaflet";
import {IRulerObj} from "@/interfaces/IRulerObj";

export class RulerCalculations{
    static iterateLatLng = (arr: LatLngExpression[]) => {
        let rulerArr:IRulerObj[] = []
        for(let i = 1; i < arr.length; ++i){
            rulerArr.push({
                pos: this.getMidpointSegment(arr[i], arr[i-1]),
                title: this.getLengthSegment(arr[i], arr[i-1])
            })
        }
        return rulerArr
    }

    static getMidpointSegment(p1: LatLngExpression, p2: LatLngExpression):LatLngExpression{
        return [(p1[0] + p2[0])/2, (p1[1] + p2[1])/2]
    }

    static getLengthSegment(p1: LatLngExpression, p2: LatLngExpression):string{
        let from = new LatLng(p1[0], p1[1])
        let to = new LatLng(p2[0], p2[1])
        console.log(parseFloat(from.distanceTo(to).toFixed(2)) + " m")
        return parseFloat(from.distanceTo(to).toFixed(2)) + " m"
    }
}
