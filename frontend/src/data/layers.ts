import {ILayer} from "@/interfaces/ILayer";
import {EUrls} from "@/enums/EUrls";


export const layers:ILayer[] = [
    {
        name: 'Standard map',
        url: EUrls.STANDARD_TILE_URL,
    },
    {
        name: 'ESRI map',
        url: EUrls.ESRI_TILE_URL,
    },
    {
        name: 'Monochrome map',
        url: EUrls.MONOCHROME_TILE_URL,
    },
]