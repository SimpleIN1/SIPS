import { describe, expect, it } from "vitest";
import mapReducer, {
  changeChecked,
  setAdditionalLayerVisible,
  setLayer,
} from "@/store/map/map-slice";
import { EUrls } from "@/enums/EUrls";

describe("map slice", () => {
  it("changes base map layer", () => {
    const state = mapReducer(undefined, setLayer(EUrls.ESRI_TILE_URL));

    expect(state.layer).toBe(EUrls.ESRI_TILE_URL);
  });

  it("turns regions layer on and off", () => {
    let state = mapReducer(
      undefined,
      setAdditionalLayerVisible({
        url: EUrls.REGIONS_URL,
        isVisible: true,
      })
    );

    expect(state.isRegions).toBe(true);
    expect(
      state.borders.find((border) => border.url === EUrls.REGIONS_URL)?.checked
    ).toBe(true);

    state = mapReducer(
      state,
      setAdditionalLayerVisible({
        url: EUrls.REGIONS_URL,
        isVisible: false,
      })
    );

    expect(state.isRegions).toBe(false);
    expect(
      state.borders.find((border) => border.url === EUrls.REGIONS_URL)?.checked
    ).toBe(false);
  });

  it("turns nature reserves layer on", () => {
    const state = mapReducer(
      undefined,
      setAdditionalLayerVisible({
        url: EUrls.NATURE_RESERVES_URL,
        isVisible: true,
      })
    );

    expect(state.isNatureReserves).toBe(true);
    expect(
      state.borders.find((border) => border.url === EUrls.NATURE_RESERVES_URL)
        ?.checked
    ).toBe(true);
  });

  it("turns settlements layer on", () => {
    const state = mapReducer(
      undefined,
      setAdditionalLayerVisible({
        url: EUrls.SETTLEMENTS_URL,
        isVisible: true,
      })
    );

    expect(state.isSettlements).toBe(true);
    expect(
      state.borders.find((border) => border.url === EUrls.SETTLEMENTS_URL)
        ?.checked
    ).toBe(true);
  });

  it("toggles additional layer by url", () => {
    let state = mapReducer(undefined, changeChecked(EUrls.REGIONS_URL));

    expect(state.isRegions).toBe(true);
    expect(
      state.borders.find((border) => border.url === EUrls.REGIONS_URL)?.checked
    ).toBe(true);

    state = mapReducer(state, changeChecked(EUrls.REGIONS_URL));

    expect(state.isRegions).toBe(false);
    expect(
      state.borders.find((border) => border.url === EUrls.REGIONS_URL)?.checked
    ).toBe(false);
  });
});
