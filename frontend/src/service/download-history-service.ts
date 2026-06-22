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

type SatelliteItem = {
  id: number;
  name?: string;
  tag?: string;
};

type CompositeItem = {
  id: number;
  name?: string;
  title?: string;
};

type TimeItem = {
  id: number;
  time?: string;
  datetime?: string;
};

type TimesResponse = {
  times?: TimeItem[];
};

type DatesResponse = {
  dates?: string[] | Record<string, Record<string, string[]>>;
};

type CreateDownloadHistoryPayload = {
  data: string;
};

const dateTimeCache = new Map<number, string>();

const getSatelliteTitle = (satellite?: SatelliteItem) => {
  if (!satellite) return "";

  return satellite.tag || satellite.name || `ID ${satellite.id}`;
};

const getCompositeTitle = (composite?: CompositeItem) => {
  if (!composite) return "";

  return composite.name || composite.title || `ID ${composite.id}`;
};

const splitSnapshotDateTime = (value: string) => {
  if (!value || value.startsWith("ID ")) {
    return {
      date: value,
      time: "",
    };
  }

  const [date = value, time = ""] = value.split(" ");

  return {
    date,
    time,
  };
};

const normalizeDates = (data: string[] | DatesResponse | unknown): string[] => {
  if (Array.isArray(data)) {
    return data;
  }

  if (!data || typeof data !== "object" || !("dates" in data)) {
    return [];
  }

  const dates = (data as DatesResponse).dates;

  if (Array.isArray(dates)) {
    return dates;
  }

  if (!dates || typeof dates !== "object") {
    return [];
  }

  return Object.values(dates)
    .flatMap((months) =>
      months && typeof months === "object"
        ? Object.values(months as Record<string, string[]>)
        : []
    )
    .flat()
    .filter((date): date is string => typeof date === "string");
};

const findDateTimeById = async (
  datetimeId: number,
  satelliteTag: string
): Promise<string> => {
  if (dateTimeCache.has(datetimeId)) {
    return dateTimeCache.get(datetimeId) || "";
  }

  if (!satelliteTag) {
    return `ID ${datetimeId}`;
  }

  const datesResponse = await api.get<string[] | DatesResponse>(
    `/vicod/dates/${satelliteTag}`
  );

  const dates = normalizeDates(datesResponse.data);

  for (const date of dates) {
    try {
      const timesResponse = await api.get<TimesResponse>(
        `/vicod/dates/times/${satelliteTag}/${date}`
      );

      const timeItem = (timesResponse.data.times ?? []).find(
        (item) => Number(item.id) === Number(datetimeId)
      );

      if (timeItem) {
        const value = timeItem.datetime || timeItem.time || `ID ${datetimeId}`;

        dateTimeCache.set(datetimeId, value);

        return value;
      }
    } catch (error) {
      console.warn(
        `Не удалось загрузить время снимка для ${satelliteTag} ${date}:`,
        error
      );
    }
  }

  return `ID ${datetimeId}`;
};

export default class DownloadHistoryService {
  static async getDownloadHistory(
    page: number,
    limit: number
  ): Promise<DownloadHistoryResponse> {
    try {
      const [historyResponse, satellitesResponse, compositesResponse] =
        await Promise.all([
          api.get<ServerDownloadHistoryResponse>(
            "/vcd/composites/download/history",
            {
              params: {
                page,
                per_page: limit,
              },
            }
          ),
          api.get<SatelliteItem[]>("/vicod/satellites"),
          api.get<CompositeItem[]>("/vicod/composites"),
        ]);

      const history = historyResponse.data;
      const satellites = satellitesResponse.data ?? [];
      const composites = compositesResponse.data ?? [];

      const items = await Promise.all(
        (history.items ?? []).map(async (item) => {
          const satellite = satellites.find(
            (satelliteItem) => satelliteItem.id === item.satellite
          );

          const composite = composites.find(
            (compositeItem) => compositeItem.id === item.composite
          );

          const satelliteTitle = getSatelliteTitle(satellite);
          const compositeTitle = getCompositeTitle(composite);

          const snapshotDateTime = await findDateTimeById(
            item.datetime_composite,
            satelliteTitle
          );

          const { date: snapshotDate, time: snapshotTime } =
            splitSnapshotDateTime(snapshotDateTime);

          return {
            id: String(item.id),
            date: item.datetime_download,
            data: [
              `Продукт: ${satelliteTitle || `спутник ID ${item.satellite}`}`,
              `Композит: ${compositeTitle || `композит ID ${item.composite}`}`,
              `Дата снимка: ${snapshotDate}`,
              snapshotTime ? `Время съемки: ${snapshotTime}` : "",
            ]
              .filter(Boolean)
              .join(" · "),
          };
        })
      );

      return {
        items,
        total: history.pagination?.total ?? history.items?.length ?? 0,
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
    return Promise.resolve();
  }
}