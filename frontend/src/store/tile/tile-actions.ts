import { createAsyncThunk } from "@reduxjs/toolkit";
import TileService from "@/service/tile-service";
import { IDates } from "@/interfaces/IDates";
import { Mark } from "@mui/base";
import { ISatelliteResponse } from "@/interfaces/ISatelliteResponse";
import { ICompositeResponse } from "@/interfaces/ICompositeResponse";

export const fetchDates = createAsyncThunk<IDates, string>(
  "tile/fetchDates",
  async (satellite: string) => {
    return await TileService.getDates(satellite);
  }
);

interface FetchTimesPayload {
  satellite: string;
  date: string;
}

export const fetchTimes = createAsyncThunk<Mark[], FetchTimesPayload>(
  "tile/fetchTimes",
  async ({ satellite, date }: FetchTimesPayload) => {
    return await TileService.getTimes(satellite, date);
  }
);

export const fetchSatellites = createAsyncThunk<ISatelliteResponse[]>(
  "tile/fetchSatellites",
  async () => {
    return await TileService.getSatellites();
  }
);

interface FetchCompositesPayload {
  satellite: string;
  dotdate: string;
  dottime: string;
}

export const fetchComposites = createAsyncThunk<
  ICompositeResponse,
  FetchCompositesPayload
>(
  "tile/fetchComposites",
  async (obj: FetchCompositesPayload) => {
    return await TileService.getComposites(
      obj.satellite,
      obj.dotdate,
      obj.dottime
    );
  }
);