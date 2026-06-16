import { describe, expect, it } from "vitest";
import { EUrls, TILE_DOMAIN } from "@/enums/EUrls";
import { buildTileUrl } from "@/utils/tileUrl";

describe("tile url builder", () => {
  it("builds VIIRS tile layer URL from selected parameters", () => {
    const url = buildTileUrl("snpp", "20230617", "0720", "vievi");

    expect(url).toBe(
      `${TILE_DOMAIN}/snpp/20230617/0720/vievi/${EUrls.VIIRS_TILE_ENDPOINT}`
    );
  });

  it("keeps leaflet tile placeholders in the URL", () => {
    const url = buildTileUrl("noaa20", "20230618", "0910", "vscmo");

    expect(url).toContain("{z}");
    expect(url).toContain("{x}");
    expect(url).toContain("{-y}.png");
  });
});
