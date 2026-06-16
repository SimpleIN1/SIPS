import { useState } from "react";
import s from "./DownloadSelectedProduct.module.scss";
import { useAppSelector } from "@/hooks/hook";
import ProductDownloadService from "@/service/product-download-service";
import DownloadHistoryService from "@/service/download-history-service";

const DownloadSelectedProduct = () => {
  const isAuth = useAppSelector((state) => state.user.isAuth);

  const satellite = useAppSelector((state) => state.tile.satellite);
  const composite = useAppSelector((state) => state.tile.composite);
  const dotDate = useAppSelector((state) => state.tile.dateTime.dotdate);
  const nonDotDate = useAppSelector((state) => state.tile.dateTime.nondotdate);
  const time = useAppSelector((state) => state.tile.dateTime.time);

  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [isError, setIsError] = useState(false);

  if (!isAuth || !satellite || !composite || !dotDate || !nonDotDate || !time) {
    return null;
  }

  const handleDownload = async () => {
    try {
      setIsLoading(true);
      setMessage(null);
      setIsError(false);

      await ProductDownloadService.downloadSelectedProduct({
        satellite: String(satellite),
        composite: String(composite),
        dotDate,
        nonDotDate,
        time,
      });

      await DownloadHistoryService.createDownloadHistoryItem({
        data: `${satellite} | ${composite} | ${dotDate} ${time}`,
      });

      setMessage("Файл скачан");
    } catch (error) {
      console.error("Ошибка скачивания выбранного продукта:", error);
      setIsError(true);
      setMessage("Не удалось скачать файл");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={s.downloadBlock}>
      <button
        type="button"
        className={s.downloadButton}
        onClick={handleDownload}
        disabled={isLoading}
      >
        {isLoading ? "Скачивание..." : "Скачать выбранный продукт"}
      </button>

      {message && (
        <div className={isError ? s.errorText : s.successText}>
          {message}
        </div>
      )}
    </div>
  );
};

export default DownloadSelectedProduct;