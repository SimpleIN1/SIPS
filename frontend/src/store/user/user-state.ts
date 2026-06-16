import { IUser } from "@/interfaces/IUser";
import { RegistrationError } from "@/interfaces/response/RegistrationError";

export interface UserState{
    user : IUser
    isAuth : boolean
    isLoading : boolean
    token : string,
    refresh : string
    err : RegistrationError
}