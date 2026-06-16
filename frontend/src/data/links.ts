import {ILink} from "@/interfaces/Ilink";

export const profileLinksAuth: ILink[] = [
    {
        id: 1,
        to: "/home",
        title: "Главная",
    },
    {
        id: 2,
        to: "/management",
        title: "Руководство пользователя",
    },
]

export const profileLinksNotAuth: ILink[] = [
    {
        id: 1,
        to: "/home",
        title: "Главная",
    },
    {
        id: 2,
        to: "/management",
        title: "Руководство пользователя",
    }
]

export const mainLinksNotAuth: ILink[] = [

    {
        id: 1,
        to: "/authorization",
        title: "Вход",
    },
]


export const mainLinksAuth: ILink[] = [
    {
        id: 1,
        to: "/profile",
        title: "Профиль",
    },
    {
        id: 2,
        to: "/authorization",
        title: "выход",
    },
]

export const navbarLinksAuth: ILink[] = [
    {
        id: 1,
        to: "/",
        title: "Перейти к карте",
    },
    
    {
        id: 3,
        to: "/profile",
        title: "Профиль",
    },
    {
        id: 4,
        to: "/home",
        title: "Главная",
    },
    {
        id: 5,
        to: "/management",
        title: "Руководство пользователя",
    },
    
]


export const navbarLinksNotAuth: ILink[] = [
    {
        id: 2,
        to: "/",
        title: "Перейти к карте",
    },
    {
        id: 3,
        to: "/profile",
        title: "Профиль",
    },
    {
        id: 4,
        to: "/home",
        title: "Главная",
    },
    {
        id: 5,
        to: "/management",
        title: "Руководство пользователя",
    },
    
]

export const headerSimpleLinks: ILink[] = [
  { id: 1, to: "/home", title: "Главная" },
  { id: 2, to: "/", title: "Перейти к карте" },
];

export const headerLinksNotAuth: ILink[] = [
  { id: 1, to: "/", title: "Перейти к карте" },
  { id: 2, to: "/home", title: "Главная" },
];

export const headerLinksAuth: ILink[] = [
  { id: 1, to: "/", title: "Перейти к карте" },
  { id: 3, to: "/home", title: "Главная" },
];