import {ESatellite} from "@/enums/ESatellite";

export interface ISatellite {
    id: string
    label: string,
    value: ESatellite,
    checked: boolean
}
