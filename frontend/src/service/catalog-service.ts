import { IImage } from "@/interfaces/IImage";
import api from "@/http";
import { IImages } from "@/interfaces/IImages";

type GenerateLinksResponse = {
  links: {
    id: number;
    link: string;
    datetime_expiration: string;
  }[];
};

export default class CatalogService {
  static async getItems(images: IImage[]): Promise<IImages> {
    const response = await api.post<GenerateLinksResponse>(
      "/vcd/composites/generate-link",
      { images }
    );

    return {
      images: response.data.links.map((item) => ({
        uid: String(item.id),
        url: item.link,
      })) as IImage[],
    };
  }

  static async getTimes(date: string) {
    const response = await api.get(`/vicod/dates/times/snpp/${date}`);
    return response.data;
  }

  static async downloadImage(image: IImage): Promise<void> {
    if (!image.url) {
      throw new Error("Невозможно скачать файл: сервер не вернул ссылку");
    }

    const response = await api.get(image.url, {
      responseType: "blob",
    });

    const blob = new Blob([response.data]);
    const downloadUrl = window.URL.createObjectURL(blob);

    const fileName = `${image.datetime}_${image.composite}_${image.satellite}.tif`
      .replaceAll(" ", "_")
      .replaceAll(":", "-");

    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = fileName;

    document.body.appendChild(a);
    a.click();
    a.remove();

    window.URL.revokeObjectURL(downloadUrl);
  }

  static async newGetItems(images: IImage[]): Promise<IImages> {
    return this.getItems(images);
  }
}