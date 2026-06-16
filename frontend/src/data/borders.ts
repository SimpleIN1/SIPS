import {IBorder} from "@/interfaces/IBorder";
import {EUrls} from "@/enums/EUrls";

export const borders: IBorder[] = [
    {
        id: "0",
        name: "Границы регионов",
        url: EUrls.REGIONS_URL,
        color: "error",
        checked: false
    },
    {
        id: "1",
        name: "Заповедники",
        url: EUrls.NATURE_RESERVES_URL,
        color: "success",
        checked: false
    },
    {
        id: "2",
        name: "Населенные пункты",
        url: EUrls.SETTLEMENTS_URL,
        color: "primary",
        checked: false
    },
]