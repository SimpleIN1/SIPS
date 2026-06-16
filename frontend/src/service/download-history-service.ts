import api from "@/http";

export type DownloadHistoryItem = {
  id: string;
  date: string;
  data: string;
};

export type DownloadHistoryResponse = {
  items: DownloadHistoryItem[];
  total: number;
};

type CreateDownloadHistoryPayload = {
  data: string;
};

export default class DownloadHistoryService {
  static async getDownloadHistory(
    page: number,
    limit: number
  ): Promise<DownloadHistoryResponse> {
    try {
      const response = await api.get<DownloadHistoryResponse>("/download-history", {
        params: {
          page,
          limit,
        },
      });

      const data = response.data;

      return {
        items: data.items ?? [],
        total: data.total ?? data.items?.length ?? 0,
      };
    } catch (error) {
      console.error("Ошибка загрузки истории скачиваний:", error);

      return {
        items: [],
        total: 0,
      };
    }
  }

  static async createDownloadHistoryItem(
    payload: CreateDownloadHistoryPayload
  ): Promise<void> {
    try {
      await api.post("/download-history", {
        date: new Date().toISOString(),
        data: payload.data,
      });
    } catch (error) {
      console.warn("История скачиваний пока не сохранена на сервере:", error);
    }
  }
}