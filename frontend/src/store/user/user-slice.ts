import { createSlice } from "@reduxjs/toolkit";
import { UserState } from "./user-state";
import { loginUser, registerUser, checkAuth, logoutUser } from "./user-actions";

const initialState: UserState = {
  user: {
    username: "",
    password: "",
    email: "",
    first_name: "",
    last_name: "",
    middle_name: "",
    organization: "",
  },
  isAuth: false,
  isLoading: false,
  token: "",
  refresh: "",
  err: null as any, // если UserState у тебя пока не string|null — оставим так, чтобы не ругалось
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    logout(state) {
      localStorage.removeItem("token");
      localStorage.removeItem("refresh");
      state.isAuth = false;
      state.token = "";
      state.refresh = "";
      state.user = initialState.user;
      state.err = null;
    },
    removeErrors(state) {
      state.err = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // LOGIN
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
        state.err = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isAuth = true;
        state.token = action.payload.access || "";
        state.refresh = action.payload.refresh || "";
        state.isLoading = false;
        state.err = null;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isAuth = false;
        state.isLoading = false;
        state.err = (action.payload as any) || "Ошибка авторизации";
      })

      // REGISTER
      .addCase(registerUser.pending, (state) => {
        state.isLoading = true;
        state.err = null;
      })
      .addCase(registerUser.fulfilled, (state) => {
        state.isLoading = false;
        state.err = null;
        state.isAuth = false; // после регистрации пусть входит через логин
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.isLoading = false;
        state.err = (action.payload as any) || "Ошибка регистрации";
      })

      // LOGOUT
      .addCase(logoutUser.fulfilled, (state) => {
        state.isAuth = false;
        state.user = initialState.user;
        state.token = "";
        state.refresh = "";
        state.isLoading = false;
        state.err = null;
      })

      // CHECK AUTH (refresh)
      .addCase(checkAuth.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(checkAuth.fulfilled, (state, action) => {
        const access = action.payload?.access || "";
        const refresh = action.payload?.refresh || "";

        state.isAuth = Boolean(access);
        state.token = access;
        if (refresh) state.refresh = refresh;

        state.isLoading = false;
      })
      .addCase(checkAuth.rejected, (state) => {
        state.isAuth = false;
        state.token = "";
        state.refresh = "";
        state.isLoading = false;
      });
  },
});

export const { logout, removeErrors } = userSlice.actions;
export default userSlice.reducer;