import { ESettingType } from "@/enums/ESettingType";
import { ISatellite } from "./ISatellite";

export interface sett{
    value: string,
    label : string
}


export interface ISetting{
    name : string,
    type : ESettingType,
    setting : sett[]
}