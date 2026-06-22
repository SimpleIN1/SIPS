import React, { useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import styles from "./RestoreAccessPage.module.scss";
import { BackArrow } from "@/components/BackArrow/BackArrow";
import AuthService from "@/service/auth-service";

type Step = "email" | "code" | "reset" | "done";

type ResetParams = {
  userId: string;
  timestamp: number;
  signature: string;
};

function isValidEmail(v: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim());
}

function useRestoreParams() {
  const { search } = useLocation();

  return useMemo(() => {
    const params = new URLSearchParams(search);

    return {
      email: (params.get("email") || "").trim(),
      userId: (params.get("user_id") || "").trim(),
      timestamp: Number(params.get("timestamp") || 0),
      signature: (params.get("signature") || "").trim(),
    };
  }, [search]);
}

export default function RestoreAccess() {
  const navigate = useNavigate();
  const { email: queryEmail, userId, timestamp, signature } = useRestoreParams();

  const hasResetParams = Boolean(userId && timestamp && signature);

  const [step, setStep] = useState<Step>(hasResetParams ? "reset" : "email");
  const [isLoading, setIsLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const [email, setEmail] = useState(queryEmail);
  const [otpCode, setOtpCode] = useState("");

  const [resetParams, setResetParams] = useState<ResetParams | null>(
    hasResetParams ? { userId, timestamp, signature } : null
  );

  const [pass1, setPass1] = useState("");
  const [pass2, setPass2] = useState("");
  const [show1, setShow1] = useState(false);
  const [show2, setShow2] = useState(false);
  const [pass1Touched, setPass1Touched] = useState(false);
  const [pass2Touched, setPass2Touched] = useState(false);

  const goBack = () => {
    if (step === "email") return navigate(-1);
    if (step === "code") return setStep("email");
    if (step === "reset") return setStep("code");
    if (step === "done") return navigate("/authorization");
  };

  const sendResetLink = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);

    const emailToUse = email.trim();

    if (!emailToUse) {
      setErr("Введите email");
      return;
    }

    if (!isValidEmail(emailToUse)) {
      setErr("Введите корректный email");
      return;
    }

    setIsLoading(true);

    try {
      await AuthService.sendResetPasswordLink({
        login: emailToUse,
      });

      setEmail(emailToUse);
      setStep("code");
    } catch (error) {
      console.error("Ошибка отправки кода восстановления:", error);
      setErr("Не удалось отправить код восстановления");
    } finally {
      setIsLoading(false);
    }
  };

  const verifyOtpCode = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);

    const emailToUse = email.trim();
    const code = otpCode.trim();

    if (!emailToUse) {
      setErr("Введите email");
      return;
    }

    if (!code) {
      setErr("Введите код из письма");
      return;
    }

    setIsLoading(true);

    try {
      const response = await AuthService.verifyResetPasswordOtp({
        email: emailToUse,
        otp_code: code,
      });

      setResetParams({
        userId: response.data.user_id,
        timestamp: response.data.timestamp,
        signature: response.data.signature,
      });

      setStep("reset");
    } catch (error) {
      console.error("Ошибка проверки кода:", error);
      setErr("Неверный код или срок действия кода истёк");
    } finally {
      setIsLoading(false);
    }
  };

  const resetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);

    if (!resetParams) {
      setErr("Код восстановления некорректен или устарел");
      return;
    }

    const p1 = pass1.trim();
    const p2 = pass2.trim();

    if (!p1) {
      setErr("Введите новый пароль");
      return;
    }

    if (p1.length < 8) {
      setErr("Пароль должен быть не короче 8 символов");
      return;
    }

    if (p1 !== p2) {
      setErr("Пароли не совпадают");
      return;
    }

    setIsLoading(true);

    try {
      await AuthService.resetPassword({
        user_id: resetParams.userId,
        timestamp: resetParams.timestamp,
        signature: resetParams.signature,
        password: p1,
      });

      setStep("done");

      setTimeout(() => {
        navigate("/authorization");
      }, 1000);
    } catch (error) {
      console.error("Ошибка восстановления пароля:", error);
      setErr("Не удалось изменить пароль. Возможно, код устарел");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.back}>
        <button
          type="button"
          onClick={goBack}
          style={{ background: "transparent", border: "none", cursor: "pointer" }}
        >
          <BackArrow />
        </button>
      </div>

      <div className={styles.card}>
        <div className={styles.tabs}>
          <Link className={styles.tab} to="/authorization">
            Авторизация
          </Link>
          <Link className={styles.tab} to="/registration">
            Регистрация
          </Link>
        </div>

        {step === "email" && (
          <>
            <h1 className={styles.title}>Восстановление доступа</h1>
            <p className={styles.subtitle}>
              Введите email аккаунта. Мы отправим код для установки нового пароля.
            </p>

            <form onSubmit={sendResetLink} className={styles.form}>
              <label className={styles.label}>
                Email
                <input
                  className={styles.input}
                  placeholder="example@mail.com"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoFocus
                />
              </label>

              {err && <div className={styles.error}>{err}</div>}

              <button
                type="submit"
                className={styles.primaryBtnWide}
                disabled={isLoading}
                aria-busy={isLoading}
              >
                {isLoading ? "Отправляем..." : "Отправить код"}
              </button>
            </form>
          </>
        )}

        {step === "code" && (
          <>
            <h1 className={styles.title}>Введите код</h1>
            <p className={styles.subtitle}>
              Мы отправили код восстановления на почту {email}.
            </p>

            <form onSubmit={verifyOtpCode} className={styles.form}>
              <label className={styles.label}>
                Код из письма
                <input
                  className={styles.input}
                  placeholder="Введите код"
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                  autoFocus
                />
              </label>

              {err && <div className={styles.error}>{err}</div>}

              <button
                type="submit"
                className={styles.primaryBtnWide}
                disabled={isLoading}
                aria-busy={isLoading}
              >
                {isLoading ? "Проверяем..." : "Подтвердить код"}
              </button>
            </form>
          </>
        )}

        {step === "reset" && (
          <>
            <h1 className={styles.title}>Новый пароль</h1>
            <p className={styles.subtitle}>
              Введите новый пароль, который будет использоваться для входа в аккаунт.
            </p>

            <form onSubmit={resetPassword} className={styles.form}>
              <label className={styles.label}>
                Новый пароль
                <div className={styles.passRow}>
                  <input
                    className={styles.inputWide}
                    type={show1 ? "text" : "password"}
                    value={pass1}
                    onChange={(e) => setPass1(e.target.value)}
                    onBlur={() => setPass1Touched(true)}
                    autoFocus
                  />
                  <button
                    type="button"
                    className={styles.eyeBtn}
                    onClick={() => setShow1((v) => !v)}
                    aria-label="Показать пароль"
                  >
                    👁
                  </button>
                </div>

                {pass1Touched && pass1.length > 0 && pass1.length < 8 && (
                  <div className={styles.hint}>Минимум 8 символов</div>
                )}
              </label>

              <label className={styles.label}>
                Повторите новый пароль
                <div className={styles.passRow}>
                  <input
                    className={styles.inputWide}
                    type={show2 ? "text" : "password"}
                    value={pass2}
                    onChange={(e) => setPass2(e.target.value)}
                    onBlur={() => setPass2Touched(true)}
                  />
                  <button
                    type="button"
                    className={styles.eyeBtn}
                    onClick={() => setShow2((v) => !v)}
                    aria-label="Показать пароль"
                  >
                    👁
                  </button>
                </div>

                {pass2Touched && pass2.length > 0 && pass1.trim() !== pass2.trim() && (
                  <div className={styles.hint}>Пароли должны совпадать</div>
                )}
              </label>

              {err && <div className={styles.error}>{err}</div>}

              <button
                type="submit"
                className={styles.primaryBtnWide}
                disabled={isLoading}
                aria-busy={isLoading}
              >
                {isLoading ? "Сохраняем..." : "Изменить пароль"}
              </button>
            </form>
          </>
        )}

        {step === "done" && (
          <>
            <h1 className={styles.title}>Готово</h1>
            <p className={styles.subtitle}>
              Пароль успешно изменён. Сейчас мы вернём вас на страницу входа.
            </p>

            <button
              type="button"
              className={styles.primaryBtnWide}
              onClick={() => navigate("/authorization")}
            >
              Перейти ко входу
            </button>
          </>
        )}
      </div>
    </div>
  );
}