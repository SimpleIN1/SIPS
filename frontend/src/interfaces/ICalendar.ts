import {Dayjs} from "dayjs";

export interface ICalendar{
    currentMonth: boolean,
    date: Dayjs,
    today: boolean
}