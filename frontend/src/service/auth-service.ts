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
  organization_name?: string;
};

export type ProfilePayload = {
  first_name?: string;
  last_name?: string;
  middle_name?: string;
  email?: string;
  organization_name?: string;
};

export type ChangePasswordPayload = {
  old_password: string;
  password: string;
  password_confirm: string;
};

export type SendResetPasswordLinkPayload = {
  login: string;
};

export type VerifyResetPasswordOtpPayload = {
  email: string;
  otp_code: string;
};

export type VerifyResetPasswordOtpResponse = {
  detail: string;
  user_id: string;
  timestamp: number;
  signature: string;
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
    return api.post<AuthorizationResponse>("/vauth/token/", {
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
      organization_name: user.organization,
    };

    return api.post<RegistrationResponse>("/vaccount/register/", payload);
  }

  static async getProfile(): Promise<AxiosResponse<IUser>> {
    return api.get<IUser>("/vaccount/profile/");
  }

  static async updateProfile(
    payload: ProfilePayload
  ): Promise<AxiosResponse<IUser>> {
    return api.patch<IUser>("/vaccount/profile/", payload);
  }

  static async changePassword(
    payload: ChangePasswordPayload
  ): Promise<AxiosResponse<void>> {
    return api.post<void>("/vaccount/change/password/", payload);
  }

  static async sendResetPasswordLink(
    payload: SendResetPasswordLinkPayload
  ): Promise<AxiosResponse<void>> {
    return api.post<void>("/vaccount/reset/password/", payload);
  }

  static async verifyResetPasswordOtp(
    payload: VerifyResetPasswordOtpPayload
  ): Promise<AxiosResponse<VerifyResetPasswordOtpResponse>> {
    return api.post<VerifyResetPasswordOtpResponse>(
      "/vaccount/reset/password/otpcode/verify/",
      payload
    );
  }

  static async resetPassword(
    payload: ResetPasswordPayload
  ): Promise<AxiosResponse<void>> {
    return api.post<void>("/vaccount/reset/password/verify/", payload);
  }

  static async verifyRegistration(
    payload: VerifyRegistrationPayload
  ): Promise<AxiosResponse<void>> {
    return api.post<void>("/vaccount/register/verify/", payload);
  }

  static async logout(): Promise<void> {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
  }

  static async refresh(
    refresh: string
  ): Promise<AxiosResponse<AuthorizationResponse>> {
    return api.post<AuthorizationResponse>("/vauth/token/refresh/", {
      refresh,
    });
  }
}