import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import dayjs from "dayjs";
import type { Mark } from "@mui/base";
import { ISatelliteResponse } from "@/interfaces/ISatelliteResponse";
import { ESatellite } from "@/enums/ESatellite";
import { EComposite } from "@/enums/EComposite";
import {
  fetchComposites,
  fetchDates,
  fetchSatellites,
  fetchTimes,
} from "@/store/tile/tile-actions";

interface DateTime {
  dotdate: string;
  nondotdate: string;
  time: string;
}

interface TileState {
  currentDate: any;
  calendar: any[];
  dotdates: string[];
  nondotdates: string[];
  dateTime: DateTime;
  times: Mark[];
  satellites: ISatelliteResponse[];
  composites: string[];
  satellite: ESatellite | null;
  composite: EComposite | null;
  isLoading: boolean;
}

const initialState: TileState = {
  currentDate: dayjs(),
  calendar: [],
  dotdates: [],
  nondotdates: [],
  dateTime: {
    dotdate: "",
    nondotdate: "",
    time: "",
  },
  times: [],
  satellites: [],
  composites: [],
  satellite: null,
  composite: null,
  isLoading: false,
};

const tileSlice = createSlice({
  name: "tile",
  initialState,

  reducers: {
    setDotDate: (state, action: PayloadAction<string>) => {
      state.dateTime.dotdate = action.payload;
      state.dateTime.nondotdate = action.payload.replace(/-/g, "");
      state.dateTime.time = "";
      state.composite = null;
      state.times = [];
      state.composites = [];
    },

    setNonDotDate: (state, action: PayloadAction<string>) => {
      state.dateTime.nondotdate = action.payload;
    },

    setTime: (state, action: PayloadAction<string>) => {
      state.dateTime.time = action.payload;
      state.composite = null;
      state.composites = [];
    },

    setSatellite: (state, action: PayloadAction<ESatellite>) => {
      state.satellite = action.payload;
      state.dateTime = {
        dotdate: "",
        nondotdate: "",
        time: "",
      };
      state.composite = null;
      state.times = [];
      state.composites = [];
    },

    setComposite: (state, action: PayloadAction<EComposite | null>) => {
      state.composite = action.payload;
    },

    toggleComposite: (state, action: PayloadAction<EComposite>) => {
      state.composite =
        state.composite === action.payload ? null : action.payload;
    },

    removeTimes: (state) => {
      state.times = [];
    },

    clearComposites: (state) => {
      state.composites = [];
      state.composite = null;
    },
  },

  extraReducers: (builder) => {
    builder
      .addCase(fetchDates.pending, (state) => {
        state.isLoading = true;
      })

      .addCase(fetchDates.fulfilled, (state, action) => {
        state.isLoading = false;

        if (!action.payload) {
          return;
        }

        state.dotdates = action.payload.dotdates ?? [];
        state.nondotdates = action.payload.nondotdates ?? [];
      })

      .addCase(fetchDates.rejected, (state) => {
        state.isLoading = false;
      })

      .addCase(fetchTimes.fulfilled, (state, action) => {
        state.times = action.payload ?? [];
      })

      .addCase(fetchTimes.rejected, (state) => {
        state.times = [];
      })

      .addCase(fetchSatellites.fulfilled, (state, action) => {
        if (action.payload && action.payload.length > 0) {
          state.satellites = action.payload;
        }
      })

      .addCase(fetchComposites.fulfilled, (state, action) => {
        state.composites = action.payload?.composites ?? [];
      })

      .addCase(fetchComposites.rejected, (state) => {
        state.composites = [];
      });
  },
});

export const {
  setDotDate,
  setNonDotDate,
  setTime,
  setSatellite,
  setComposite,
  toggleComposite,
  removeTimes,
  clearComposites,
} = tileSlice.actions;

export default tileSlice.reducer;