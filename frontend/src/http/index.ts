import axios from "axios";
import type { InternalAxiosRequestConfig } from "axios";
import { API_URL } from "@/shared/config";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: false,
});

const publicAuthEndpoints = [
  "/vauth/token/",
  "/vaccount/register/",
  "/vaccount/register/verify/",
  "/vaccount/register-email/",
  "/vaccount/register-email/verify/",
  "/vaccount/reset-password/send-link/",
  "/vaccount/reset-password/",
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

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._isRetry
    ) {
      originalRequest._isRetry = true;

      const refresh = localStorage.getItem("refresh");

      if (!refresh) {
        return Promise.reject(error);
      }

      try {
        const response = await axios.post(`${API_URL}/vauth/token/refresh/`, {
          refresh,
        });

        const access = response.data.access;
        const newRefresh = response.data.refresh;

        localStorage.setItem("token", access);

        if (newRefresh) {
          localStorage.setItem("refresh", newRefresh);
        }

        originalRequest.headers.set("Authorization", `Bearer ${access}`);

        return api.request(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem("token");
        localStorage.removeItem("refresh");

        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
