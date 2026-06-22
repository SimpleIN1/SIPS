import type { ChangeEvent } from "react";
import s from "./TimeLine.module.scss";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { setTime } from "@/store/tile/tile-slice";
import { fetchComposites } from "@/store/tile/tile-actions";
import { Mark } from "@mui/base";

interface TimeLineProps {
  disabled?: boolean;
}

const normalizeTime = (value: unknown): string => {
  if (typeof value !== "string" && typeof value !== "number") {
    return "";
  }

  const raw = String(value);

  if (raw.includes(":")) {
    const [hours, minutes] = raw.split(":");
    return `${hours.padStart(2, "0")}${minutes.padStart(2, "0")}`;
  }

  const onlyDigits = raw.replace(/\D/g, "");

  if (onlyDigits.length < 4) {
    return "";
  }

  return onlyDigits.slice(0, 4);
};

const formatTimeLabel = (time: string): string => {
  if (time.length !== 4) {
    return time;
  }

  return `${time.slice(0, 2)}:${time.slice(2, 4)}`;
};

const TimeLine = ({ disabled = false }: TimeLineProps) => {
  const dispatch = useAppDispatch();

  const satellite = useAppSelector((state) => state.tile.satellite);
  const dotdate = useAppSelector((state) => state.tile.dateTime.dotdate);
  const times: Mark[] = useAppSelector((state) => state.tile.times) || [];
  const selectedTime = useAppSelector((state) => state.tile.dateTime.time);

  const normalizedTimes = times
    .map((time) => {
      const normalizedValue = normalizeTime(time.label);

      return {
        label: formatTimeLabel(normalizedValue),
        value: normalizedValue,
      };
    })
    .filter((time) => time.value);

  const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;

    dispatch(setTime(value));

    if (!value || !satellite || !dotdate) {
      return;
    }

    dispatch(
      fetchComposites({
        satellite,
        dotdate,
        dottime: value,
      })
    );
  };

  return (
    <div className={s.timeBlock}>
      <label className={s.label}>Время съёмки</label>

      {disabled ? (
        <div className={s.emptyTime}>Сначала выберите дату</div>
      ) : normalizedTimes.length > 0 ? (
        <select
          className={s.select}
          value={selectedTime || ""}
          onChange={handleChange}
        >
          <option value="">Выберите время</option>

          {normalizedTimes.map((time) => (
            <option key={time.value} value={time.value}>
              {time.label}
            </option>
          ))}
        </select>
      ) : (
        <div className={s.emptyTime}>
          Для выбранной даты время не найдено
        </div>
      )}
    </div>
  );
};

export default TimeLine;