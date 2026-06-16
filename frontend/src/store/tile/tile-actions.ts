import { createAsyncThunk } from "@reduxjs/toolkit";
import TileService from "@/service/tile-service";
import { IDates } from "@/interfaces/IDates";
import { Mark } from "@mui/base";
import { ISatelliteResponse } from "@/interfaces/ISatelliteResponse";
import { ICompositeResponse } from "@/interfaces/ICompositeResponse";

export const fetchDates = createAsyncThunk<IDates, string | undefined>(
  "tile/fetchDates",
  async () => {
    return await TileService.getDates();
  }
);

export const fetchTimes = createAsyncThunk<Mark[], string>(
  "tile/fetchTimes",
  async (date: string) => {
    return await TileService.getTimes(date);
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