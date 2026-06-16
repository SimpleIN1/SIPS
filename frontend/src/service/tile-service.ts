import api from "@/http";
import { IDates } from "@/interfaces/IDates";
import { Mark } from "@mui/base";
import { ISatelliteResponse } from "@/interfaces/ISatelliteResponse";
import { ICompositeResponse } from "@/interfaces/ICompositeResponse";
import { ESatellite } from "@/enums/ESatellite";

type DatesServerResponse = {
  dates: Record<string, Record<string, Record<string, string[]>>>;
};

type TimesServerResponse = {
  times: string[];
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

const normalizeDates = (data: IDates | DatesServerResponse): IDates => {
  if ("dotdates" in data && "nondotdates" in data) {
    return {
      dotdates: data.dotdates ?? [],
      nondotdates: data.nondotdates ?? [],
    };
  }

  if ("dates" in data) {
    const dotdates = Object.values(data.dates)
      .flatMap((months) => Object.values(months))
      .flatMap((weeks) => Object.values(weeks))
      .flat()
      .sort();

    const nondotdates = dotdates.map((date) => date.replace(/-/g, ""));

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
  return time.replace("-", ":");
};

const normalizeTimes = (data: TimesServerResponse | string[] | any): Mark[] => {
  const times = Array.isArray(data) ? data : data?.times;

  if (!Array.isArray(times)) {
    return [];
  }

  return times.map((item) => {
    const label = normalizeTimeLabel(String(item));

    return {
      label,
      value: timeToSliderValue(label),
    };
  });
};

const toServerTime = (time: string): string => {
  if (time.includes("-")) {
    return time;
  }

  if (time.includes(":")) {
    return time.replace(":", "-");
  }

  if (time.length === 4) {
    return `${time.slice(0, 2)}-${time.slice(2)}`;
  }

  return time;
};

export default class TileService {
  static async getDates(): Promise<IDates> {
    try {
      const response = await api.get<IDates | DatesServerResponse>("/vicod/dates");

      return normalizeDates(response.data);
    } catch (error) {
      console.warn(
        "Не удалось загрузить даты с сервера, используется fallback:",
        error
      );

      return FALLBACK_DATES;
    }
  }

  static async getTimes(date: string): Promise<Mark[]> {
    try {
      const response = await api.get<TimesServerResponse>(
        `/vicod/dates/${date}/times`
      );

      const times = normalizeTimes(response.data);

      console.log(`Доступное время для даты ${date}:`, times);

      return times;
    } catch (error) {
      console.warn("Не удалось загрузить время с сервера:", error);

      if (date === "2023-06-17") {
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
      const response = await api.get<ISatelliteResponse[]>("/vicod/satellites");

      return response.data;
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
    try {
      const serverTime = toServerTime(time);

      const response = await api.get<ICompositeResponse>(
        `/vicod/composites/${satellite}/${date}/${serverTime}`
      );

      return {
        composites: response.data.composites ?? [],
      };
    } catch (error) {
      console.warn(
        "Не удалось загрузить композиты с сервера, используется fallback:",
        error
      );

      return FALLBACK_COMPOSITES;
    }
  }
}