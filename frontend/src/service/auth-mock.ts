import { IUser } from "@/interfaces/IUser";

type Tokens = { access: string; refresh: string };

const wait = (ms = 350) => new Promise((r) => setTimeout(r, ms));

export const AuthMock = {
  async login(email: string, password: string): Promise<Tokens> {
    await wait();
    if (!email || !password) throw new Error("bad_credentials");
    return { access: "mock_access_token", refresh: "mock_refresh_token" };
  },

  async registration(user: IUser): Promise<{ ok: true }> {
    await wait();
    if (!user.email || !user.password) throw new Error("bad_data");
    return { ok: true };
  },

  async logout(): Promise<void> {
    await wait(150);
  },

  async refresh(refresh: string | null): Promise<Tokens> {
    await wait(150);
    if (!refresh) return { access: "", refresh: "" };
    return { access: "mock_access_token", refresh: "mock_refresh_token" };
  },
};