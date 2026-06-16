import { useEffect, useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import styles from "./RestoreAccessPage.module.scss";
import AuthService from "@/service/auth-service";

type VerifyStatus = "loading" | "success" | "error";

function useVerifyParams() {
  const { search } = useLocation();

  return useMemo(() => {
    const normalizedSearch = search
      .replace(/×tamp/g, "&timestamp")
      .replace(/%C3%97tamp/g, "&timestamp");

    const params = new URLSearchParams(normalizedSearch);

    return {
      userId: (params.get("user_id") || "").trim(),
      timestamp: Number(params.get("timestamp") || 0),
      signature: (params.get("signature") || "").trim(),
    };
  }, [search]);
}

export default function VerifyUser() {
  const navigate = useNavigate();
  const { userId, timestamp, signature } = useVerifyParams();

  const [status, setStatus] = useState<VerifyStatus>("loading");
  const [message, setMessage] = useState("Подтверждаем аккаунт...");

  useEffect(() => {
    let isMounted = true;

    const verifyUser = async () => {
      if (!userId || !timestamp || !signature) {
        setStatus("error");
        setMessage("Ссылка подтверждения некорректна или устарела");
        return;
      }

      try {
        await AuthService.verifyRegistration({
          user_id: userId,
          timestamp,
          signature,
        });

        if (!isMounted) return;

        setStatus("success");
        setMessage("Аккаунт успешно подтверждён. Сейчас перенаправим вас на страницу входа.");

        setTimeout(() => {
          navigate("/authorization");
        }, 1500);
      } catch (error) {
        console.error("Ошибка подтверждения регистрации:", error);

        if (!isMounted) return;

        setStatus("error");
        setMessage("Не удалось подтвердить аккаунт. Возможно, ссылка устарела.");
      }
    };

    verifyUser();

    return () => {
      isMounted = false;
    };
  }, [navigate, userId, timestamp, signature]);

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.tabs}>
          <Link className={styles.tab} to="/authorization">
            Авторизация
          </Link>
          <Link className={styles.tab} to="/registration">
            Регистрация
          </Link>
        </div>

        <h1 className={styles.title}>
          {status === "loading" && "Подтверждение аккаунта"}
          {status === "success" && "Готово"}
          {status === "error" && "Ошибка подтверждения"}
        </h1>

        <p className={styles.subtitle}>{message}</p>

        {status !== "loading" && (
          <button
            type="button"
            className={styles.primaryBtnWide}
            onClick={() => navigate("/authorization")}
          >
            Перейти ко входу
          </button>
        )}
      </div>
    </div>
  );
}