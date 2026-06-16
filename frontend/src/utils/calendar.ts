import dayjs from "dayjs";
import { ICalendar } from "@/interfaces/ICalendar";
import { IDate } from "@/interfaces/IDate";
import { Mark } from "@mui/base";
import { ISettingDates } from "@/interfaces/ISettingDates";

export const generateDate = (
  month: number = dayjs().month(),
  year: number = dayjs().year()
): ICalendar[] => {
  const first = dayjs().year(year).month(month).startOf("month");
  const last = dayjs().year(year).month(month).endOf("month");
  const arrayOfDate: ICalendar[] = [];

  for (let i = 1; i < first.day(); i++) {
    arrayOfDate.push({ currentMonth: false, date: first.day(i), today: false });
  }

  for (let i = first.date(); i <= last.date(); i++) {
    const d = first.date(i);
    arrayOfDate.push({
      currentMonth: true,
      date: d,
      today: d.toDate().toDateString() === dayjs().toDate().toDateString(),
    });
  }

  const remaining = 42 - arrayOfDate.length;
  for (let i = 1; i <= remaining; i++) {
    arrayOfDate.push({ currentMonth: false, date: last.add(i, "day"), today: false });
  }

  return arrayOfDate;
};

export const getStringDate = (date: dayjs.Dayjs): string => {
  const year = date.year();
  const month = (date.month() + 1).toString().padStart(2, "0");
  const day = date.date().toString().padStart(2, "0");
  return `${year}${month}${day}`;
};

export const convertNumber = (num: string): string => {
  return Number(num) < 10 ? "0" + num : num;
};

// Самая важная функция — теперь максимально толерантная
export const isThereDataForThisDay = (day: string, dateArray: string[]): boolean => {
  if (!dateArray || dateArray.length === 0 || !day) return false;

  const cleanDay = day.replace(/[^0-9]/g, "");

  return dateArray.some((el) => {
    const cleanEl = el.replace(/[^0-9]/g, "");
    return cleanEl === cleanDay;
  });
};

export const getMarksByDate = (selectedDate: string, dateArray: IDate[]): Mark[] => {
  const found = dateArray.find((el) => el.date === selectedDate);
  return found?.times ?? [];
};

export const getMinValue = (marks: Mark[]): number => {
  if (!marks?.length) return 0;
  return Math.min(...marks.map(el => el.value));
};

export const getMaxValue = (marks: Mark[]): number => {
  if (!marks?.length) return 100;
  return Math.max(...marks.map(el => el.value));
};

export const getMarksWithEqualIntervals = (marks: Mark[]): Mark[] => {
  if (!marks?.length) return [];
  if (marks.length === 1) return marks;

  const min = getMinValue(marks);
  const max = getMaxValue(marks);
  const step = (max - min) / (marks.length - 1);

  return marks.map((mark, i) => ({
    value: min + step * i,
    label: String(mark.label ?? ""),
  }));
};

export const days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"];

export const months = [
  "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
  "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
];

export const convert = (el: string): { str: string; value: number } => {
  const year = el.substring(0, 4);
  const month = el.substring(5, 7);
  const day = el.substring(8, 10);
  const value = Number(day) + Number(month) * 30 + Number(year) + 365;
  return { str: `${day}-${month}-${year}`, value };
};

export const convertDates = (arr: string[]): ISettingDates[] => {
  const strs: ISettingDates[] = arr.map((el) => {
    const conv = convert(el);
    return { reverse: el, normal: conv.str, value: conv.value };
  });
  return strs.sort((a, b) => a.value - b.value);
};