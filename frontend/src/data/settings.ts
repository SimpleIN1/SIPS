import { ISetting, sett } from "@/interfaces/ISetting";
import { satellites } from "./satellites";
import { Composites } from "./composites";
import { ESettingType } from "@/enums/ESettingType";



const getSatellitesSett = (): sett[] => {
    let arr:sett[] = []
    satellites.forEach((el) => arr.push({value : el.value, label: el.label}))
    return arr
}
const getCompositesSett = (): sett[] => {
    let arr:sett[] = []
    Composites.forEach((el) => arr.push({value : el, label: el}))
    return arr
}




export const settings : ISetting[] = [
    {
        name: "спутник",
        type : ESettingType.SATTELITE,
        setting : getSatellitesSett()
    },
    {
        name : "композит",
        type : ESettingType.COMPOSITE,
        setting : getCompositesSett()
    }
]