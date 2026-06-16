import { ICatalogItem } from "@/interfaces/ICatalogItem";
import { IImage } from "@/interfaces/IImage";
import { IImages } from "@/interfaces/IImages";
import { ISatellite } from "@/interfaces/ISatellite";

export interface CatalogState{
    sattelite : string,
    composite : string,
    start_day : string,
    end_day : string
    catalogItems : IImage[]
    images : IImage[]
    datetimes : string[]
    imagesObj: IImages
    
}