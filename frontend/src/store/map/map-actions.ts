import { createAsyncThunk } from "@reduxjs/toolkit";
import MapService from "@/service/map-service";

export const fetchRegions = createAsyncThunk(
  "map/fetchRegions",
  async (url: string) => {
    const response = await MapService.getRegions(url);

    return {
      response: response.data,
      url,
    };
  }
);