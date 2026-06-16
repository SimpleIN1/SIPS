import {ISatellite} from "@/interfaces/ISatellite";
import {ESatellite} from "@/enums/ESatellite";

export const satellites : ISatellite[] = [
    {
        id: "0",
        label: "Suoimi NPP",
        value: ESatellite.SUOMI_NPP,
        checked: false
    },
    {
        id: "1",
        label: "NOAA-20",
        value: ESatellite.NOAA_20,
        checked: false
    }
]