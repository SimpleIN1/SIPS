import api from "@/http";
import { IImage } from "@/interfaces/IImage";

type SelectedProductPayload = {
  satellite: string;
  composite: string;
  dotDate: string;
  nonDotDate: string;
  time: string;
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

export default class ProductDownloadService {
  static async downloadSelectedProduct(payload: SelectedProductPayload) {
    const imageRequest: IImage = {
      datetime: `${payload.dotDate} ${payload.time}`,
      satellite: payload.satellite,
      composite: payload.composite,
    };

    const urlsResponse = await api.post<{ images: IImage[] }>(
      "/vCD/composites/urls",
      {
        images: [imageRequest],
      }
    );

    const image = urlsResponse.data.images?.[0];

    if (!image) {
      throw new Error("Сервер не вернул данные для скачивания");
    }

    const fileName = `${payload.nonDotDate}_${payload.time}_${payload.satellite}_${payload.composite}.tif`
      .replaceAll(" ", "_")
      .replaceAll(":", "-");

    if (image.uid) {
      const fileResponse = await api.get(
        `/vCD/composites/download/${image.uid}`,
        {
          responseType: "blob",
        }
      );

      downloadBlob(fileResponse.data, fileName);
      return image;
    }

    if (image.url) {
      const fileResponse = await api.get(image.url, {
        responseType: "blob",
      });

      downloadBlob(fileResponse.data, fileName);
      return image;
    }

    throw new Error("У изображения нет uid или url для скачивания");
  }
}