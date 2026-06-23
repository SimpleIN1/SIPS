import api from "@/http";

type SelectedProductPayload = {
  satellite: string;
  composite: string;
  dotDate: string;
  nonDotDate: string;
  time: string;
};

type Satellite = {
  id: number;
  name: string;
  tag: string;
};

type Composite = {
  id: number;
  name: string;
};

type TimeItem = {
  time: string;
  datetime: string;
  id: number;
};

type TimesResponse = {
  times: TimeItem[];
};

type GenerateLinksResponse = {
  links: {
    id: number;
    link: string;
    datetime_expiration: string;
  }[];
};

const downloadBlob = (blob: Blob, fileName: string) => {
  const downloadUrl = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = downloadUrl;
  a.download = fileName;

  document.body.appendChild(a);
  a.click();
  a.remove();

  window.URL.revokeObjectURL(downloadUrl);
};

const normalizeTime = (time: string) =>
  String(time).replace(/\D/g, "").slice(0, 4);

export default class ProductDownloadService {
  static async downloadSelectedProduct(payload: SelectedProductPayload) {
    const satellitesResponse = await api.get<Satellite[]>("/vicod/satellites");

    const satelliteItem = satellitesResponse.data.find(
      (item) => item.tag === payload.satellite || item.name === payload.satellite
    );

    if (!satelliteItem) {
      throw new Error(`Спутник не найден: ${payload.satellite}`);
    }

    const compositesResponse = await api.get<Composite[]>("/vicod/composites");

    const compositeItem = compositesResponse.data.find(
      (item) => item.name === payload.composite
    );

    if (!compositeItem) {
      throw new Error(`Композит не найден: ${payload.composite}`);
    }

    const timesResponse = await api.get<TimesResponse>(
      `/vicod/dates/times/${payload.satellite}/${payload.dotDate}`
    );

    const selectedTime = normalizeTime(payload.time);

    const datetimeItem = timesResponse.data.times.find(
      (item) => normalizeTime(item.time) === selectedTime
    );

    if (!datetimeItem) {
      throw new Error(`Время не найдено: ${payload.time}`);
    }

    const urlsResponse = await api.post<GenerateLinksResponse>(
      "/vcd/composites/generate-link",
      {
        images: [
          {
            datetime: datetimeItem.id,
            satellite: satelliteItem.id,
            composite: compositeItem.id,
          },
        ],
      }
    );

    const link = urlsResponse.data.links?.[0];

    if (!link) {
      throw new Error("Сервер не вернул ссылку для скачивания");
    }

    const fileName = `${payload.nonDotDate}_${payload.time}_${payload.satellite}_${payload.composite}.tif`
      .replaceAll(" ", "_")
      .replaceAll(":", "-");

    const fileResponse = await api.get(link.link, {
      responseType: "blob",
    });

    downloadBlob(fileResponse.data, fileName);

    return {
      datetime: String(datetimeItem.id),
      satellite: String(satelliteItem.id),
      composite: String(compositeItem.id),
      uid: String(link.id),
      url: link.link,
    };
  }
}