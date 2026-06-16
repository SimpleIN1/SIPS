import { describe, expect, it } from "vitest";
import userReducer, { logout, removeErrors } from "@/store/user/user-slice";
import { checkAuth, loginUser, registerUser } from "@/store/user/user-actions";

describe("user slice", () => {
  it("stores access and refresh tokens after successful login", () => {
    let state = userReducer(
      undefined,
      loginUser.pending("request-id", {
        email: "student@example.ru",
        password: "1234",
      })
    );

    expect(state.isLoading).toBe(true);
    expect(state.err).toBeNull();

    state = userReducer(
      state,
      loginUser.fulfilled(
        {
          access: "access-token",
          refresh: "refresh-token",
        } as any,
        "request-id",
        {
          email: "student@example.ru",
          password: "1234",
        }
      )
    );

    expect(state.isAuth).toBe(true);
    expect(state.token).toBe("access-token");
    expect(state.refresh).toBe("refresh-token");
    expect(state.isLoading).toBe(false);
    expect(state.err).toBeNull();
  });

  it("stores login error after failed authorization", () => {
    const state = userReducer(
      undefined,
      loginUser.rejected(
        null,
        "request-id",
        {
          email: "bad@example.ru",
          password: "wrong",
        },
        "Ошибка авторизации" as any
      )
    );

    expect(state.isAuth).toBe(false);
    expect(state.isLoading).toBe(false);
    expect(state.err).toBe("Ошибка авторизации");
  });

  it("does not authorize user after successful registration", () => {
    const state = userReducer(
      undefined,
      registerUser.fulfilled(
        { ok: true },
        "request-id",
        {
          username: "student",
          password: "1234",
          email: "student@example.ru",
          first_name: "Елизавета",
          last_name: "Герасимова",
          middle_name: "",
          organization: "",
        }
      )
    );

    expect(state.isAuth).toBe(false);
    expect(state.isLoading).toBe(false);
    expect(state.err).toBeNull();
  });

  it("clears auth state and tokens after logout", () => {
    localStorage.setItem("token", "access-token");
    localStorage.setItem("refresh", "refresh-token");

    let state = userReducer(
      undefined,
      loginUser.fulfilled(
        {
          access: "access-token",
          refresh: "refresh-token",
        } as any,
        "request-id",
        {
          email: "student@example.ru",
          password: "1234",
        }
      )
    );

    state = userReducer(state, logout());

    expect(state.isAuth).toBe(false);
    expect(state.token).toBe("");
    expect(state.refresh).toBe("");
    expect(state.err).toBeNull();
    expect(localStorage.getItem("token")).toBeNull();
    expect(localStorage.getItem("refresh")).toBeNull();
  });

  it("updates auth state after successful refresh check", () => {
    const state = userReducer(
      undefined,
      checkAuth.fulfilled(
        {
          access: "new-access-token",
          refresh: "new-refresh-token",
        } as any,
        "request-id"
      )
    );

    expect(state.isAuth).toBe(true);
    expect(state.token).toBe("new-access-token");
    expect(state.refresh).toBe("new-refresh-token");
    expect(state.isLoading).toBe(false);
  });

  it("clears errors and resets auth when refresh check fails", () => {
    let state = userReducer(
      undefined,
      loginUser.rejected(
        null,
        "request-id",
        {
          email: "bad@example.ru",
          password: "wrong",
        },
        "Ошибка авторизации" as any
      )
    );

    state = userReducer(state, removeErrors());

    expect(state.err).toBeNull();

    state = userReducer(state, checkAuth.rejected(null, "request-id"));

    expect(state.isAuth).toBe(false);
    expect(state.token).toBe("");
    expect(state.refresh).toBe("");
    expect(state.isLoading).toBe(false);
  });
});
