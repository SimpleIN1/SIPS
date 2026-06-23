import { useState, ChangeEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import styles from "./AuthorizationPage.module.scss";
import { BackArrow } from "@/components/BackArrow/BackArrow";
import { useAppDispatch } from "@/hooks/hook";
import { loginUser } from "@/store/user/user-actions";

type LoginForm = {
  email: string;
  password: string;
};

const Authorization = () => {
  const [form, setForm] = useState<LoginForm>({ email: "", password: "" });
  const [err, setErr] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);

  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const handleChange: React.ChangeEventHandler<HTMLInputElement> = (
    e: ChangeEvent<HTMLInputElement>
  ) => {
    setForm((p) => ({ ...p, [e.target.name]: e.target.value }));
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);

    const action = await dispatch(
      loginUser({ email: form.email, password: form.password } as any)
    );

    if (loginUser.fulfilled.match(action)) {
      navigate("/profile");
    } else {
      setErr("Неверный email или пароль");
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.back}>
        <BackArrow />
      </div>

      <div className={styles.card}>
        <div className={styles.tabs}>
          <div className={styles.tabActive}>Авторизация</div>
          <Link className={styles.tab} to="/registration">
            Регистрация
          </Link>
        </div>

        <h1 className={styles.title}>Вход в аккаунт</h1>
        <p className={styles.subtitle}>
          Введите email и пароль, чтобы продолжить
        </p>

        <form onSubmit={onSubmit} className={styles.form}>
          <label className={styles.label}>
            Email
            <input
              className={styles.input}
              placeholder="example@mail.com"
              type="text"
              name="email"
              value={form.email}
              onChange={handleChange}
              autoComplete="email"
            />
          </label>

          <label className={styles.label}>
            Пароль
            <div className={styles.passRow}>
              <input
                className={styles.inputWide}
                placeholder="••••••••"
                type={showPassword ? "text" : "password"}
                name="password"
                value={form.password}
                onChange={handleChange}
                autoComplete="current-password"
              />
              <button
                type="button"
                className={styles.eyeBtn}
                onClick={() => setShowPassword((value) => !value)}
                aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
              >
                👁
              </button>
            </div>
          </label>

          {err && <div className={styles.error}>{err}</div>}

          <button type="submit" className={styles.primaryBtn}>
            Войти
          </button>

          <div className={styles.links}>
            <span>Забыли пароль?</span>
            <Link
              to={
                form.email.trim()
                  ? `/restore?email=${encodeURIComponent(form.email.trim())}`
                  : "/restore"
              }
            >
              Восстановить доступ
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Authorization;