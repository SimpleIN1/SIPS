import api from "@/http";
import { IDates } from "@/interfaces/IDates";
import { Mark } from "@mui/base";
import { ISatelliteResponse } from "@/interfaces/ISatelliteResponse";
import { ICompositeResponse } from "@/interfaces/ICompositeResponse";
import { ESatellite } from "@/enums/ESatellite";

type UnknownRecord = Record<string, unknown>;

type DatesServerResponse = {
  dotdates?: string[];
  nondotdates?: string[];
  dates?: unknown;
};

type TimesServerResponse = {
  times?: unknown;
};

type SatellitesServerResponse = {
  satellites?: unknown;
};

type CompositesServerResponse = {
  composites?: unknown;
};

const FALLBACK_DATES: IDates = {
  dotdates: [
    "2023-06-17",
    "2023-06-18",
    "2023-06-19",
    "2023-06-20",
    "2023-06-21",
    "2023-06-22",
    "2023-06-23",
    "2023-06-24",
    "2023-06-25",
    "2023-06-26",
    "2023-06-27",
    "2023-06-28",
    "2023-06-29",
    "2023-06-30",
  ],
  nondotdates: [
    "20230617",
    "20230618",
    "20230619",
    "20230620",
    "20230621",
    "20230622",
    "20230623",
    "20230624",
    "20230625",
    "20230626",
    "20230627",
    "20230628",
    "20230629",
    "20230630",
  ],
};

const FALLBACK_SATELLITES: ISatelliteResponse[] = [
  {
    id: 1,
    name: "Suomi NPP",
    tag: ESatellite.SUOMI_NPP,
  },
  {
    id: 2,
    name: "NOAA-20",
    tag: ESatellite.NOAA_20,
  },
];

const FALLBACK_COMPOSITES: ICompositeResponse = {
  composites: [
    "aot550",
    "aotaps",
    "clphs",
    "clmsk",
    "clmsk2",
    "frmsk",
    "vievi",
    "vindvi",
    "vlst",
    "vscmo",
  ],
};

const isRecord = (value: unknown): value is UnknownRecord => {
  return typeof value === "object" && value !== null && !Array.isArray(value);
};

const collectStringValues = (value: unknown): string[] => {
  if (Array.isArray(value)) {
    return value.flatMap((item) => collectStringValues(item));
  }

  if (isRecord(value)) {
    return Object.values(value).flatMap((item) => collectStringValues(item));
  }

  if (typeof value === "string") {
    return [value];
  }

  return [];
};

const unique = (items: string[]): string[] => {
  return Array.from(new Set(items));
};

const toDotDate = (date: string): string => {
  const value = date.trim();

  if (/^\d{8}$/.test(value)) {
    return `${value.slice(0, 4)}-${value.slice(4, 6)}-${value.slice(6, 8)}`;
  }

  return value;
};

const toNoDotDate = (date: string): string => {
  return date.trim().replace(/-/g, "");
};

const normalizeDates = (data: DatesServerResponse | string[] | unknown): IDates => {
  if (isRecord(data)) {
    const dotdates = Array.isArray(data.dotdates)
      ? data.dotdates.map((date) => String(date))
      : [];

    const nondotdates = Array.isArray(data.nondotdates)
      ? data.nondotdates.map((date) => String(date))
      : [];

    if (dotdates.length > 0 || nondotdates.length > 0) {
      const normalizedDotDates =
        dotdates.length > 0 ? dotdates.map(toDotDate) : nondotdates.map(toDotDate);

      const normalizedNoDotDates =
        nondotdates.length > 0
          ? nondotdates.map(toNoDotDate)
          : normalizedDotDates.map(toNoDotDate);

      return {
        dotdates: unique(normalizedDotDates).sort(),
        nondotdates: unique(normalizedNoDotDates).sort(),
      };
    }

    if ("dates" in data) {
      const dates = collectStringValues(data.dates);

      const dotdates = unique(dates.map(toDotDate)).sort();
      const nondotdates = unique(dotdates.map(toNoDotDate)).sort();

      return {
        dotdates,
        nondotdates,
      };
    }
  }

  if (Array.isArray(data)) {
    const dates = data.map((date) => String(date));

    const dotdates = unique(dates.map(toDotDate)).sort();
    const nondotdates = unique(dotdates.map(toNoDotDate)).sort();

    return {
      dotdates,
      nondotdates,
    };
  }

  return {
    dotdates: [],
    nondotdates: [],
  };
};

const timeToSliderValue = (time: string): number => {
  return Number(time.replace(/[:\-]/g, ""));
};

const normalizeTimeLabel = (time: string): string => {
  const value = time.trim().replace("-", ":");

  if (/^\d{4}$/.test(value)) {
    return `${value.slice(0, 2)}:${value.slice(2, 4)}`;
  }

  if (/^\d{3}$/.test(value)) {
    const padded = value.padStart(4, "0");
    return `${padded.slice(0, 2)}:${padded.slice(2, 4)}`;
  }

  return value;
};

const normalizeTimes = (data: TimesServerResponse | string[] | unknown): Mark[] => {
  const source = isRecord(data) && "times" in data ? data.times : data;

  if (!Array.isArray(source)) {
    return [];
  }

  const times = source
    .map((item) => {
      if (typeof item === "string") {
        return item;
      }

      if (isRecord(item) && typeof item.time === "string") {
        return item.time;
      }

      return "";
    })
    .filter(Boolean);

  return unique(times).map((item) => {
    const label = normalizeTimeLabel(String(item));

    return {
      label,
      value: timeToSliderValue(label),
    };
  });
};

const toServerTime = (time: string): string => {
  const value = String(time).trim().replace(":", "").replace("-", "");

  if (/^\d{3}$/.test(value)) {
    return value.padStart(4, "0");
  }

  return value;
};

const normalizeSatellites = (
  data: SatellitesServerResponse | unknown
): ISatelliteResponse[] => {
  const source = isRecord(data) && "satellites" in data ? data.satellites : data;

  if (!Array.isArray(source)) {
    return [];
  }

  return source.reduce<ISatelliteResponse[]>((acc, item, index) => {
    if (typeof item === "string") {
      acc.push({
        id: index + 1,
        name: item,
        tag: item,
      });

      return acc;
    }

    if (!isRecord(item)) {
      return acc;
    }

    const tag = String(item.tag ?? item.value ?? item.code ?? item.name ?? "");
    const name = String(item.name ?? item.title ?? tag);

    if (!tag) {
      return acc;
    }

    acc.push({
      id: Number(item.id ?? index + 1),
      name,
      tag,
    });

    return acc;
  }, []);
};

const normalizeComposites = (
  data: CompositesServerResponse | string[] | unknown
): ICompositeResponse => {
  const source = isRecord(data) && "composites" in data ? data.composites : data;
  const composites = unique(collectStringValues(source)).sort();

  return {
    composites,
  };
};

export default class TileService {
  static async getDates(satellite: string): Promise<IDates> {
    if (!satellite) {
      return {
        dotdates: [],
        nondotdates: [],
      };
    }

    try {
      const response = await api.get<DatesServerResponse | string[]>(
        `/vicod/dates/${satellite}`
      );

      return normalizeDates(response.data);
    } catch (error) {
      console.warn(
        "Не удалось загрузить даты с сервера, используется fallback:",
        error
      );

      return FALLBACK_DATES;
    }
  }

  static async getTimes(satellite: string, date: string): Promise<Mark[]> {
    if (!satellite || !date) {
      return [];
    }

    try {
      const response = await api.get<TimesServerResponse | string[]>(
        `/vicod/dates/times/${satellite}/${date}`
      );

      const times = normalizeTimes(response.data);

      console.log(
        `Доступное время для спутника ${satellite} и даты ${date}:`,
        times
      );

      return times;
    } catch (error) {
      console.warn("Не удалось загрузить время с сервера:", error);

      if (satellite === ESatellite.SUOMI_NPP && date === "2023-06-17") {
        return [
          {
            label: "07:20",
            value: 720,
          },
        ];
      }

      return [];
    }
  }

  static async getSatellites(): Promise<ISatelliteResponse[]> {
    try {
      const response = await api.get<SatellitesServerResponse | ISatelliteResponse[]>(
        "/vicod/satellites"
      );

      const satellites = normalizeSatellites(response.data);

      return satellites.length > 0 ? satellites : FALLBACK_SATELLITES;
    } catch (error) {
      console.warn(
        "Не удалось загрузить спутники с сервера, используется fallback:",
        error
      );

      return FALLBACK_SATELLITES;
    }
  }

  static async getComposites(
    satellite: string,
    date: string,
    time: string
  ): Promise<ICompositeResponse> {
    if (!satellite || !date || !time) {
      return {
        composites: [],
      };
    }

    try {
      const serverTime = toServerTime(time);

      const response = await api.get<CompositesServerResponse | string[]>(
        `/vicod/composites/${satellite}/${date}/${serverTime}`
      );

      const composites = normalizeComposites(response.data);

      return composites.composites.length > 0 ? composites : FALLBACK_COMPOSITES;
    } catch (error) {
      console.warn(
        "Не удалось загрузить композиты с сервера, используется fallback:",
        error
      );

      return FALLBACK_COMPOSITES;
    }
  }
}