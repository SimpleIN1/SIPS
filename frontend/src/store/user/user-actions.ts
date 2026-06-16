import { createAsyncThunk } from "@reduxjs/toolkit";
import AuthService from "@/service/auth-service";
import { AuthMock } from "@/service/auth-mock";
import { USE_MOCK_AUTH } from "@/shared/config";
import { IUser } from "@/interfaces/IUser";

// LOGIN
export const loginUser = createAsyncThunk(
  "user/login",
  async (payload: { email: string; password: string }, thunkAPI) => {
    try {
      const data = USE_MOCK_AUTH
        ? await AuthMock.login(payload.email, payload.password)
        : (await AuthService.login(payload.email, payload.password)).data;

      const access = data.access || "";
      const refresh = data.refresh || "";

      if (access) {
        localStorage.setItem("token", access);
      }

      if (refresh) {
        localStorage.setItem("refresh", refresh);
      }

      return {
        ...data,
        access,
        refresh,
      };
    } catch {
      return thunkAPI.rejectWithValue("Ошибка авторизации");
    }
  }
);

// REGISTER
export const registerUser = createAsyncThunk(
  "user/register",
  async (user: IUser, thunkAPI) => {
    try {
      if (USE_MOCK_AUTH) {
        await AuthMock.registration(user);
        return { ok: true };
      }

      return (await AuthService.registration(user)).data;
    } catch {
      return thunkAPI.rejectWithValue("Ошибка регистрации");
    }
  }
);

// LOGOUT
export const logoutUser = createAsyncThunk("user/logout", async () => {
  try {
    if (USE_MOCK_AUTH) {
      await AuthMock.logout();
    } else {
      await AuthService.logout();
    }
  } finally {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
  }
});

// CHECK AUTH
export const checkAuth = createAsyncThunk("user/checkAuth", async () => {
  try {
    const refreshToken = localStorage.getItem("refresh");

    if (!refreshToken) {
      return {
        access: "",
        refresh: "",
      };
    }

    const data = USE_MOCK_AUTH
      ? await AuthMock.refresh(refreshToken)
      : (await AuthService.refresh(refreshToken)).data;

    const access = data.access || "";
    const refresh = data.refresh || "";

    if (access) {
      localStorage.setItem("token", access);
    }

    if (refresh) {
      localStorage.setItem("refresh", refresh);
    }

    return {
      ...data,
      access,
      refresh,
    };
  } catch {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");

    return {
      access: "",
      refresh: "",
    };
  }
});