import { ChangeEvent, useEffect, useState } from "react";
import styles from "./ProfilePage.module.scss";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { logoutUser } from "@/store/user/user-actions";
import { useNavigate } from "react-router-dom";
import AuthService from "@/service/auth-service";
import { ConfirmLogoutModal } from "@/components/ConfirmLogoutModal/ConfirmLogoutModal";
import DownloadHistoryService, {
  type DownloadHistoryItem,
} from "@/service/download-history-service";

type ProfileTab = "profile" | "history";

const ITEMS_PER_PAGE = 10;

const getAvatarLetter = (firstName?: string, email?: string): string => {
  const value = String(firstName || email || "").trim();

  return (value.charAt(0) || "Л").toUpperCase();
};

export default function Profile() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const user = useAppSelector((s) => s.user.user);

  const [activeTab, setActiveTab] = useState<ProfileTab>("profile");

  const [photoUrl, setPhotoUrl] = useState<string | null>(null);
  const [confirmOpen, setConfirmOpen] = useState(false);

  const [downloadHistory, setDownloadHistory] = useState<DownloadHistoryItem[]>([]);
  const [historyTotal, setHistoryTotal] = useState(0);
  const [historyPage, setHistoryPage] = useState(1);
  const [isHistoryLoading, setIsHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState<string | null>(null);

  const [personalForm, setPersonalForm] = useState({
    last_name: user?.last_name || "",
    first_name: user?.first_name || "",
    middle_name: user?.middle_name || "",
    organization: user?.organization || "",
    email: user?.email || "",
  });

  const [passwordForm, setPasswordForm] = useState({
    old_password: "",
    new_password: "",
    new_password2: "",
  });

  const [personalMsg, setPersonalMsg] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  const [passwordMsg, setPasswordMsg] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  const [isSavingPersonal, setIsSavingPersonal] = useState(false);
  const [isSavingPassword, setIsSavingPassword] = useState(false);

  useEffect(() => {
    let isMounted = true;

    const loadProfile = async () => {
      try {
        const response = await AuthService.getProfile();
        const profile = response.data;

        if (!isMounted) return;

        setPersonalForm((prev) => ({
          ...prev,
          last_name: profile.last_name || "",
          first_name: profile.first_name || "",
          middle_name: profile.middle_name || "",
          organization: profile.organization || "",
          email: profile.email || "",
        }));
      } catch (error) {
        console.error("Ошибка загрузки профиля:", error);
      }
    };

    loadProfile();

    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    const saved = localStorage.getItem("userPhoto");

    if (saved?.startsWith("data:image/")) {
      setPhotoUrl(saved);
      return;
    }

    localStorage.removeItem("userPhoto");
    setPhotoUrl(null);
  }, []);

  useEffect(() => {
    if (activeTab !== "history") return;

    let isMounted = true;

    const loadHistory = async () => {
      try {
        setIsHistoryLoading(true);
        setHistoryError(null);

        const response = await DownloadHistoryService.getDownloadHistory(
          historyPage,
          ITEMS_PER_PAGE
        );

        if (!isMounted) return;

        setDownloadHistory(response.items);
        setHistoryTotal(response.total);
      } catch (error) {
        if (!isMounted) return;

        setDownloadHistory([]);
        setHistoryTotal(0);
        setHistoryError("Не удалось загрузить историю скачиваний");
      } finally {
        if (isMounted) {
          setIsHistoryLoading(false);
        }
      }
    };

    loadHistory();

    return () => {
      isMounted = false;
    };
  }, [activeTab, historyPage]);

  const totalHistoryPages = Math.max(
    1,
    Math.ceil(historyTotal / ITEMS_PER_PAGE)
  );

  const openProfileTab = () => {
    setActiveTab("profile");
  };

  const openHistoryTab = () => {
    setHistoryPage(1);
    setActiveTab("history");
  };

  const goPrevHistoryPage = () => {
    setHistoryPage((page) => Math.max(page - 1, 1));
  };

  const goNextHistoryPage = () => {
    setHistoryPage((page) => Math.min(page + 1, totalHistoryPages));
  };

  const onPickPhoto = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (!file || !file.type.startsWith("image/")) return;

    const reader = new FileReader();

    reader.onload = () => {
      const result = String(reader.result || "");

      setPhotoUrl(result);
      localStorage.setItem("userPhoto", result);
    };

    reader.readAsDataURL(file);
    e.target.value = "";
  };

  const onDeletePhoto = () => {
    setPhotoUrl(null);
    localStorage.removeItem("userPhoto");
  };

  const isValidEmail = (email: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const handlePersonalSave = async () => {
    setPersonalMsg(null);

    if (!personalForm.first_name || !personalForm.last_name || !personalForm.email) {
      setPersonalMsg({
        type: "error",
        text: "Фамилия, имя и email обязательны для заполнения",
      });
      return;
    }

    if (!isValidEmail(personalForm.email)) {
      setPersonalMsg({
        type: "error",
        text: "Введите корректный email",
      });
      return;
    }

    setIsSavingPersonal(true);

    try {
      const response = await AuthService.updateProfile({
        last_name: personalForm.last_name,
        first_name: personalForm.first_name,
        middle_name: personalForm.middle_name,
        email: personalForm.email,
      });

      const updatedProfile = response.data;

      setPersonalForm((prev) => ({
        ...prev,
        last_name: updatedProfile.last_name || "",
        first_name: updatedProfile.first_name || "",
        middle_name: updatedProfile.middle_name || "",
        email: updatedProfile.email || "",
      }));

      setPersonalMsg({
        type: "success",
        text: "Данные успешно обновлены ✓",
      });

      window.dispatchEvent(new Event("profileUpdated"));
    } catch (error) {
      console.error("Ошибка обновления профиля:", error);

      setPersonalMsg({
        type: "error",
        text: "Не удалось обновить данные профиля",
      });
    } finally {
      setIsSavingPersonal(false);
    }
  };

  const handlePasswordSave = async () => {
    setPasswordMsg(null);

    if (
      !passwordForm.old_password ||
      !passwordForm.new_password ||
      !passwordForm.new_password2
    ) {
      setPasswordMsg({
        type: "error",
        text: "Заполните все поля",
      });
      return;
    }

    if (passwordForm.new_password.length < 6) {
      setPasswordMsg({
        type: "error",
        text: "Новый пароль должен быть минимум 6 символов",
      });
      return;
    }

    if (passwordForm.new_password !== passwordForm.new_password2) {
      setPasswordMsg({
        type: "error",
        text: "Пароли не совпадают",
      });
      return;
    }

    setIsSavingPassword(true);

    try {
      await AuthService.changePassword({
        old_password: passwordForm.old_password,
        password: passwordForm.new_password,
        password_confirm: passwordForm.new_password2,
      });

      setPasswordMsg({
        type: "success",
        text: "Пароль успешно изменён ✓",
      });

      setPasswordForm({
        old_password: "",
        new_password: "",
        new_password2: "",
      });
    } catch (error) {
      console.error("Ошибка смены пароля:", error);

      setPasswordMsg({
        type: "error",
        text: "Не удалось изменить пароль",
      });
    } finally {
      setIsSavingPassword(false);
    }
  };

  const onLogout = async () => {
    await dispatch(logoutUser());
    setConfirmOpen(false);
    navigate("/");
  };

  return (
    <div className={styles.page}>
      <div
        className={`${styles.content} ${
          activeTab === "history" ? styles.historyMode : ""
        }`}
      >
        {activeTab === "profile" && (
          <div className={styles.avatarSection}>
            <div className={styles.avatarBig}>
              {photoUrl ? (
                <img src={photoUrl} alt="Аватар пользователя" />
              ) : (
                <div className={styles.avatarFallbackBig}>
                  {getAvatarLetter(personalForm.first_name, personalForm.email)}
                </div>
              )}
            </div>

            <label className={styles.uploadLabel}>
              Загрузить фото
              <input type="file" accept="image/*" onChange={onPickPhoto} />
            </label>

            {photoUrl && (
              <button className={styles.deleteBtn} onClick={onDeletePhoto}>
                Удалить фото
              </button>
            )}
          </div>
        )}

        <div
          className={`${styles.mainSection} ${
            activeTab === "history" ? styles.mainSectionHistory : ""
          }`}
        >
          {activeTab === "profile" && (
            <>
              <div className={styles.section}>
                <h2 className={styles.sectionTitle}>Личные данные</h2>

                {personalMsg && (
                  <div
                    className={
                      personalMsg.type === "success"
                        ? styles.successMsg
                        : styles.errorMsg
                    }
                  >
                    {personalMsg.text}
                  </div>
                )}

                <div className={styles.grid}>
                  <Field
                    label="Фамилия *"
                    value={personalForm.last_name}
                    onChange={(e) =>
                      setPersonalForm({
                        ...personalForm,
                        last_name: e.target.value,
                      })
                    }
                  />

                  <Field
                    label="Имя *"
                    value={personalForm.first_name}
                    onChange={(e) =>
                      setPersonalForm({
                        ...personalForm,
                        first_name: e.target.value,
                      })
                    }
                  />

                  <Field
                    label="Отчество"
                    value={personalForm.middle_name}
                    onChange={(e) =>
                      setPersonalForm({
                        ...personalForm,
                        middle_name: e.target.value,
                      })
                    }
                  />

                  <Field
                    label="Организация"
                    value={personalForm.organization}
                    onChange={(e) =>
                      setPersonalForm({
                        ...personalForm,
                        organization: e.target.value,
                      })
                    }
                  />

                  <Field
                    label="Email *"
                    value={personalForm.email}
                    type="email"
                    onChange={(e) =>
                      setPersonalForm({
                        ...personalForm,
                        email: e.target.value,
                      })
                    }
                  />
                </div>

                <button
                  className={styles.saveBtn}
                  onClick={handlePersonalSave}
                  disabled={isSavingPersonal}
                >
                  {isSavingPersonal ? "Сохранение..." : "Сохранить изменения"}
                </button>
              </div>

              <div className={styles.section}>
                <h2 className={styles.sectionTitle}>Смена пароля</h2>

                {passwordMsg && (
                  <div
                    className={
                      passwordMsg.type === "success"
                        ? styles.successMsg
                        : styles.errorMsg
                    }
                  >
                    {passwordMsg.text}
                  </div>
                )}

                <div className={styles.grid}>
                  <Field
                    label="Старый пароль"
                    value={passwordForm.old_password}
                    type="password"
                    onChange={(e) =>
                      setPasswordForm({
                        ...passwordForm,
                        old_password: e.target.value,
                      })
                    }
                  />

                  <Field
                    label="Новый пароль"
                    value={passwordForm.new_password}
                    type="password"
                    onChange={(e) =>
                      setPasswordForm({
                        ...passwordForm,
                        new_password: e.target.value,
                      })
                    }
                  />

                  <Field
                    label="Повторите новый пароль"
                    value={passwordForm.new_password2}
                    type="password"
                    onChange={(e) =>
                      setPasswordForm({
                        ...passwordForm,
                        new_password2: e.target.value,
                      })
                    }
                  />
                </div>

                <button
                  className={styles.saveBtn}
                  onClick={handlePasswordSave}
                  disabled={isSavingPassword}
                >
                  {isSavingPassword ? "Сохранение..." : "Сменить пароль"}
                </button>
              </div>
            </>
          )}

          {activeTab === "history" && (
            <div className={styles.historySection}>
              <div className={styles.historyHeader}>
                <div>Дата</div>
                <div>Данные</div>
              </div>

              {isHistoryLoading ? (
                <div className={styles.historyState}>
                  Загружаем историю скачиваний...
                </div>
              ) : historyError ? (
                <div className={styles.historyError}>
                  {historyError}
                </div>
              ) : downloadHistory.length === 0 ? (
                <div className={styles.emptyHistory}>
                  История скачиваний пока пустая
                </div>
              ) : (
                <>
                  <div className={styles.historyList}>
                    {downloadHistory.map((item) => (
                      <div className={styles.historyRow} key={item.id}>
                        <div>{item.date}</div>
                        <div>{item.data}</div>
                      </div>
                    ))}
                  </div>

                  {totalHistoryPages > 1 && (
                    <div className={styles.pagination}>
                      <button
                        type="button"
                        onClick={goPrevHistoryPage}
                        disabled={historyPage === 1 || isHistoryLoading}
                      >
                        ‹
                      </button>

                      <span className={styles.activePage}>{historyPage}</span>
                      <span>из {totalHistoryPages}</span>

                      <button
                        type="button"
                        onClick={goNextHistoryPage}
                        disabled={
                          historyPage === totalHistoryPages || isHistoryLoading
                        }
                      >
                        ›
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </div>

        <div className={styles.sidebar}>
          <div
            className={`${styles.sidebarItem} ${
              activeTab === "profile" ? styles.sidebarItemActive : ""
            }`}
            onClick={openProfileTab}
          >
            Личный кабинет
          </div>

          <div
            className={`${styles.sidebarItem} ${
              activeTab === "history" ? styles.sidebarItemActive : ""
            }`}
            onClick={openHistoryTab}
          >
            История скачиваний
          </div>

          <div className={styles.logout} onClick={() => setConfirmOpen(true)}>
            Выход из аккаунта
          </div>
        </div>
      </div>

      <ConfirmLogoutModal
        open={confirmOpen}
        onClose={() => setConfirmOpen(false)}
        onConfirm={onLogout}
      />
    </div>
  );
}

type FieldProps = {
  label: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  type?: string;
};

function Field({ label, value, onChange, type = "text" }: FieldProps) {
  const [showPassword, setShowPassword] = useState(false);
  const isPassword = type === "password";

  return (
    <div className={styles.field}>
      <label className={styles.fieldLabel}>{label}</label>

      {isPassword ? (
        <div className={styles.passRow}>
          <input
            className={styles.inputWide}
            value={value}
            onChange={onChange}
            type={showPassword ? "text" : "password"}
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
      ) : (
        <input
          className={styles.input}
          value={value}
          onChange={onChange}
          type={type}
        />
      )}
    </div>
  );
}