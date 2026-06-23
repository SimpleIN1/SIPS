import { useState, ChangeEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import styles from "./RegistrationPage.module.scss";
import { BackArrow } from "@/components/BackArrow/BackArrow";
import { useAppDispatch } from "@/hooks/hook";
import { registerUser } from "@/store/user/user-actions";
import { IUser } from "@/interfaces/IUser";

const Registration = () => {
  const [form, setForm] = useState<IUser>({
    username: "",
    password: "",
    email: "",
    first_name: "",
    last_name: "",
    middle_name: "",
    organization: "",
  });

  const [err, setErr] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
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
    setOk(null);

    if (!form.email || !form.password || !form.first_name || !form.last_name) {
      setErr("Заполни обязательные поля: Email, Пароль, Имя, Фамилия");
      return;
    }

    const action = await dispatch(registerUser(form));

    if (registerUser.fulfilled.match(action)) {
      setOk("Регистрация успешна. Теперь войдите в аккаунт.");
      setTimeout(() => navigate("/authorization"), 600);
    } else {
      setErr("Не удалось зарегистрироваться. Проверь данные.");
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.back}>
        <BackArrow />
      </div>

      <div className={styles.card}>
        <div className={styles.tabs}>
          <Link className={styles.tab} to="/authorization">
            Авторизация
          </Link>
          <div className={styles.tabActive}>Регистрация</div>
        </div>

        <h1 className={styles.title}>Создание аккаунта</h1>
        <p className={styles.subtitle}>Заполните данные, чтобы зарегистрироваться</p>

        <form onSubmit={onSubmit} className={styles.form}>
          <div className={styles.grid2}>
            <label className={styles.label}>
              Фамилия*
              <input
                className={styles.input}
                name="last_name"
                value={form.last_name}
                onChange={handleChange}
                placeholder="Иванов"
              />
            </label>

            <label className={styles.label}>
              Имя*
              <input
                className={styles.input}
                name="first_name"
                value={form.first_name}
                onChange={handleChange}
                placeholder="Иван"
              />
            </label>
          </div>

          <label className={styles.label}>
            Отчество
            <input
              className={styles.input}
              name="middle_name"
              value={form.middle_name}
              onChange={handleChange}
              placeholder="Иванович"
            />
          </label>

          <label className={styles.label}>
            Организация
            <input
              className={styles.input}
              name="organization"
              value={form.organization}
              onChange={handleChange}
              placeholder="Компания / ВУЗ"
            />
          </label>

          <label className={styles.label}>
            Email*
            <input
              className={styles.input}
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="example@mail.com"
              autoComplete="email"
            />
          </label>

          <label className={styles.label}>
            Пароль*
            <div className={styles.passRow}>
              <input
                className={styles.inputWide}
                type={showPassword ? "text" : "password"}
                name="password"
                value={form.password}
                onChange={handleChange}
                placeholder="••••••••"
                autoComplete="new-password"
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
          {ok && <div className={styles.ok}>{ok}</div>}

          <button type="submit" className={styles.primaryBtn}>
            Зарегистрироваться
          </button>

          <div className={styles.links}>
            <span>Уже есть аккаунт?</span>
            <Link to="/authorization">Войти</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Registration;