import { EUrls, TILE_DOMAIN } from "@/enums/EUrls";

export const buildTileUrl = (
  satellite: string,
  date: string,
  time: string,
  composite: string
): string => {
  return `${TILE_DOMAIN}/${satellite}/${date}/${time}/${composite}/${EUrls.VIIRS_TILE_ENDPOINT}`;
};
