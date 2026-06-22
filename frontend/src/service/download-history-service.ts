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

type ServerDownloadHistoryItem = {
  id: number;
  datetime_download: string;
  datetime_composite: number;
  satellite: number;
  composite: number;
  is_object_cut: boolean;
};

type ServerDownloadHistoryResponse = {
  items: ServerDownloadHistoryItem[];
  pagination?: {
    total?: number;
    pages?: number;
    page?: number;
    has_next?: boolean;
    has_prev?: boolean;
  };
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
      const response = await api.get<ServerDownloadHistoryResponse>(
        "/vcd/composites/download/history",
      );

      const data = response.data;

      return {
        items: (data.items ?? []).map((item) => ({
          id: String(item.id),
          date: item.datetime_download,
          data: `Спутник: ${item.satellite}, композит: ${item.composite}, дата/время: ${item.datetime_composite}`,
        })),
        total: data.pagination?.total ?? data.items?.length ?? 0,
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
    _payload: CreateDownloadHistoryPayload
  ): Promise<void> {
    // В новом API отдельного POST /download-history нет.
    // История создаётся backend автоматически при генерации/скачивании ссылки.
    return Promise.resolve();
  }
}