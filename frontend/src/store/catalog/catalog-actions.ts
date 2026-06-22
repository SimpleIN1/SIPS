import { IImage } from "@/interfaces/IImage";
import CatalogService from "@/service/catalog-service";
import TileService from "@/service/tile-service";
import { createAsyncThunk } from "@reduxjs/toolkit";
import DownloadHistoryService from "@/service/download-history-service";

interface FetchCatalogTimesPayload {
  satellite: string;
  dates: string[];
}

export const fetchCatalogItems = createAsyncThunk(
  "catalog/fetchCatalogItems",
  async (images: IImage[]) => {
    try {
      return await CatalogService.newGetItems(images);
    } catch (err) {
      console.log("fetchCatalogItems failed " + err);
      return { images: [] };
    }
  }
);

export const fetchCatalogTimes = createAsyncThunk(
  "catalog/fetchCatalogTimes",
  async ({ satellite, dates }: FetchCatalogTimesPayload) => {
    try {
      if (!satellite || dates.length === 0) {
        return [];
      }

      const arr = await Promise.all(
        dates.map(async (date) => {
          const response = await TileService.getTimes(satellite, date);
          return response.map((time) => `${date} ${time.label}`);
        })
      );

      return arr.flat();
    } catch (ex) {
      console.log(ex);
      return [];
    }
  }
);

export const downloadImage = createAsyncThunk(
  "catalog/downloadImage",
  async (image: IImage, thunkAPI) => {
    try {
      await CatalogService.downloadImage(image);

      await DownloadHistoryService.createDownloadHistoryItem({
        data: `${image.satellite} | ${image.composite} | ${image.datetime}`,
      });

      return image;
    } catch (err) {
      console.error("Ошибка скачивания:", err);
      return thunkAPI.rejectWithValue("Не удалось скачать файл");
    }
  }
);