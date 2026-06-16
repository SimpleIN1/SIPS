import api from "@/http";
import { AxiosResponse } from "axios";
import { AuthorizationResponse } from "@/interfaces/response/AuthorizationResponse";
import { RegistrationResponse } from "@/interfaces/response/RegistrationResponse";
import { IUser } from "@/interfaces/IUser";

type RegisterPayload = {
  password?: string;
  password_confirm?: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  middle_name?: string;
};

export type ProfilePayload = {
  first_name?: string;
  last_name?: string;
  middle_name?: string;
  email?: string;
};

export type ChangePasswordPayload = {
  old_password: string;
  password: string;
  password_confirm: string;
};

export type SendResetPasswordLinkPayload = {
  login: string;
};

export type ResetPasswordPayload = {
  user_id: string;
  timestamp: number;
  signature: string;
  password: string;
};

export type VerifyRegistrationPayload = {
  user_id: string;
  timestamp: number;
  signature: string;
};

export default class AuthService {
  static async login(
    email: string,
    password: string
  ): Promise<AxiosResponse<AuthorizationResponse>> {
    return api.post<AuthorizationResponse>("/account/auth/token/", {
      email,
      password,
    });
  }

  static async registration(
    user: IUser
  ): Promise<AxiosResponse<RegistrationResponse>> {
    const payload: RegisterPayload = {
      password: user.password,
      password_confirm: user.password,
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      middle_name: user.middle_name,
    };

    return api.post<RegistrationResponse>("/account/register/", payload);
  }

  static async getProfile(): Promise<AxiosResponse<IUser>> {
    return api.get<IUser>("/account/profile/");
  }

  static async updateProfile(
    payload: ProfilePayload
  ): Promise<AxiosResponse<IUser>> {
    return api.patch<IUser>("/account/profile/", payload);
  }

    static async changePassword(
    payload: ChangePasswordPayload
  ): Promise<AxiosResponse<void>> {
    return api.post<void>("/account/change-password/", payload);
  }

    static async sendResetPasswordLink(
    payload: SendResetPasswordLinkPayload
  ): Promise<AxiosResponse<void>> {
    return api.post<void>("/account/reset-password/send-link/", payload);
  }

  static async resetPassword(
    payload: ResetPasswordPayload
  ): Promise<AxiosResponse<void>> {
    return api.post<void>("/account/reset-password/", payload);
  }

    static async verifyRegistration(
    payload: VerifyRegistrationPayload
  ): Promise<AxiosResponse<void>> {
    return api.post<void>("/account/register/verify/", payload);
  }

  static async logout(): Promise<void> {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
  }

  static async refresh(
    refresh: string
  ): Promise<AxiosResponse<AuthorizationResponse>> {
    return api.post<AuthorizationResponse>("/account/auth/token/refresh/", {
      refresh,
    });
  }
}
