import { TILE_URL } from "@/shared/config";

export const TILE_DOMAIN = TILE_URL;

export enum EUrls {
  VIIRS_TILE_ENDPOINT = "{z}/{x}/{-y}.png",

  VIIRS_TILE_URL = `${TILE_DOMAIN}/snpp/20230617/0720/aot550/{z}/{x}/{-y}.png`,

  STANDARD_TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

  ESRI_TILE_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",

  MONOCHROME_TILE_URL = "https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",

  REGIONS_URL = "https://raw.githubusercontent.com/DeadEndjke/ru-regions-json/main/regions.json",

  NATURE_RESERVES_URL = "https://raw.githubusercontent.com/DeadEndjke/ru-regions-json/main/natureReserves.json",

  SETTLEMENTS_URL = "https://raw.githubusercontent.com/DeadEndjke/ru-regions-json/main/cities.json",

  DATES_URL = "https://raw.githubusercontent.com/DeadEndjke/ru-regions-json/main/dates.json",
}