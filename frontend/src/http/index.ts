import axios from "axios";
import type { InternalAxiosRequestConfig } from "axios";
import { API_URL } from "@/shared/config";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: false,
});

const publicAuthEndpoints = [
  "/account/auth/token/",
  "/account/auth/token/refresh/",
  "/account/auth/token/verify/",
  "/account/register/",
  "/account/register/verify/",
  "/account/register-email/",
  "/account/register-email/verify/",
  "/account/reset-password/send-link/",
  "/account/reset-password/",
];

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem("token");
  const url = config.url || "";

  const isPublicAuthEndpoint = publicAuthEndpoints.some((endpoint) =>
    url.startsWith(endpoint)
  );

  if (token && !token.startsWith("mock_") && !isPublicAuthEndpoint) {
    config.headers.set("Authorization", `Bearer ${token}`);
  }

  return config;
});

export default api;