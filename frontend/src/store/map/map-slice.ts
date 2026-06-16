import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { MapState } from "@/store/map/map-state";
import { fetchRegions } from "@/store/map/map-actions";
import { borders } from "@/data/borders";
import { EUrls } from "@/enums/EUrls";

type SetAdditionalLayerPayload = {
  url: EUrls | string;
  isVisible: boolean;
};

const initialState: MapState = {
  layer: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

  polygons: {
    regions: [],
    natureReserves: [],
    settlements: [],
  },

  borders: borders,

  isLoading: false,
  isRegions: false,
  isNatureReserves: false,
  isSettlements: false,
};

const setVisibilityByUrl = (
  state: MapState,
  url: EUrls | string,
  isVisible: boolean
) => {
  switch (url) {
    case EUrls.REGIONS_URL:
      state.isRegions = isVisible;
      break;

    case EUrls.NATURE_RESERVES_URL:
      state.isNatureReserves = isVisible;
      break;

    case EUrls.SETTLEMENTS_URL:
      state.isSettlements = isVisible;
      break;

    default:
      break;
  }
};

const setBorderCheckedByUrl = (
  state: MapState,
  url: EUrls | string,
  isVisible: boolean
) => {
  const border = state.borders.find((item) => item.url === url);

  if (border) {
    border.checked = isVisible;
  }
};

const mapSlice = createSlice({
  name: "map",

  initialState,

  reducers: {
    setLayer: (state, action: PayloadAction<string>) => {
      state.layer = action.payload;
    },

    setAdditionalLayerVisible: (
      state,
      action: PayloadAction<SetAdditionalLayerPayload>
    ) => {
      const { url, isVisible } = action.payload;

      setVisibilityByUrl(state, url, isVisible);
      setBorderCheckedByUrl(state, url, isVisible);
    },

    // Старые actions оставляем, чтобы старые импорты не ломались
    changeChecked: (state, action: PayloadAction<EUrls | string>) => {
      const url = action.payload;

      switch (url) {
        case EUrls.REGIONS_URL:
          state.isRegions = !state.isRegions;
          setBorderCheckedByUrl(state, url, state.isRegions);
          break;

        case EUrls.NATURE_RESERVES_URL:
          state.isNatureReserves = !state.isNatureReserves;
          setBorderCheckedByUrl(state, url, state.isNatureReserves);
          break;

        case EUrls.SETTLEMENTS_URL:
          state.isSettlements = !state.isSettlements;
          setBorderCheckedByUrl(state, url, state.isSettlements);
          break;

        default:
          break;
      }
    },

    refreshRegions: (state, action: PayloadAction<EUrls | string>) => {
      const url = action.payload;

      setVisibilityByUrl(state, url, true);
      setBorderCheckedByUrl(state, url, true);
    },

    changeCheckedBorder: (state, action: PayloadAction<number>) => {
      const index = action.payload;
      const border = state.borders[index];

      if (!border) {
        return;
      }

      border.checked = !border.checked;
      setVisibilityByUrl(state, border.url, border.checked);
    },
  },

  extraReducers: (builder) => {
    builder
      .addCase(fetchRegions.pending, (state) => {
        state.isLoading = true;
      })

      .addCase(fetchRegions.fulfilled, (state, action) => {
        state.isLoading = false;

        if (!action.payload?.response) {
          return;
        }

        const { url, response } = action.payload;

        switch (url) {
          case EUrls.REGIONS_URL:
            state.polygons.regions = response;
            break;

          case EUrls.NATURE_RESERVES_URL:
            state.polygons.natureReserves = response;
            break;

          case EUrls.SETTLEMENTS_URL:
            state.polygons.settlements = response;
            break;

          default:
            break;
        }
      })

      .addCase(fetchRegions.rejected, (state) => {
        state.isLoading = false;
      });
  },
});

export const {
  setLayer,
  setAdditionalLayerVisible,
  changeChecked,
  refreshRegions,
  changeCheckedBorder,
} = mapSlice.actions;

export const toggleLayer = changeChecked;
export const toggleBorder = changeCheckedBorder;

export default mapSlice.reducer;