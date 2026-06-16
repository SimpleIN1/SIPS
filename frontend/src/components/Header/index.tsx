import { useMemo, useState, useEffect } from "react";
import styles from "./Header.module.scss";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { headerLinksAuth, headerLinksNotAuth } from "@/data/links";
import { useAppSelector, useAppDispatch } from "@/hooks/hook";
import { logoutUser } from "@/store/user/user-actions";
import ivtLogo from "@/assets/ivt-logo.svg";
import sipsLogo from "@/assets/sips-logo.svg";
import { ConfirmLogoutModal } from "@/components/ConfirmLogoutModal/ConfirmLogoutModal";
import AuthService from "@/service/auth-service";

type HeaderProfile = {
  first_name?: string;
  email?: string;
} | null;
const Header = () => {
  const dispatch = useAppDispatch();
  const location = useLocation();
  const navigate = useNavigate();

  const isAuth = useAppSelector((state) => state.user.isAuth);
  const user = useAppSelector((state) => state.user.user);
  const [profileUser, setProfileUser] = useState<HeaderProfile>(null);

  const [photoUrl, setPhotoUrl] = useState<string | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [confirmOpen, setConfirmOpen] = useState(false);

  useEffect(() => {
    const loadPhoto = () => {
      const saved = localStorage.getItem("userPhoto");
      setPhotoUrl(saved);
    };

    loadPhoto();

    window.addEventListener("storage", loadPhoto);
    const interval = setInterval(loadPhoto, 400);

    return () => {
      window.removeEventListener("storage", loadPhoto);
      clearInterval(interval);
    };
  }, []);

  useEffect(() => {
  if (!isAuth) {
    setProfileUser(null);
    return;
  }

  let isMounted = true;

  const loadProfile = async () => {
    try {
      const response = await AuthService.getProfile();

      if (!isMounted) return;

      setProfileUser(response.data);
    } catch (error) {
      console.error("Ошибка загрузки профиля в шапке:", error);
    }
  };

  loadProfile();

  const handleProfileUpdated = () => {
    loadProfile();
  };

  window.addEventListener("profileUpdated", handleProfileUpdated);

  return () => {
    isMounted = false;
    window.removeEventListener("profileUpdated", handleProfileUpdated);
  };
}, [isAuth]);

  const links = isAuth ? headerLinksAuth : headerLinksNotAuth;

  const avatarLetter = useMemo(() => {
  const name =
    profileUser?.first_name?.trim() ||
    user?.first_name?.trim() ||
    profileUser?.email?.trim() ||
    user?.email?.trim() ||
    "";

  return (name.charAt(0) || "Л").toUpperCase();
}, [profileUser, user]);

  const goToProfile = () => {
    setMenuOpen(false);
    navigate("/profile");
  };

  const openLogoutModal = () => {
    setMenuOpen(false);
    setConfirmOpen(true);
  };

  const handleConfirmLogout = async () => {
    setConfirmOpen(false);
    localStorage.removeItem("userPhoto");
    await dispatch(logoutUser());
    navigate("/");
  };

  const goToLogin = () => {
    setMenuOpen(false);
    navigate("/authorization");
  };

  return (
    <>
      <header className={styles.root}>
        <div className={styles.inner}>
          <Link to="/home" className={styles.brand}>
            <img className={styles.logoImg} src={ivtLogo} alt="ИВТ" />

            <img className={styles.sipsLogoImg} src={sipsLogo} alt="SIPS" />
          </Link>

          <div className={styles.projectTitle}>
            <div className={styles.projectEn}>
              Satellite Image Processing System
            </div>

            <div className={styles.projectRu}>
              Система обработки спутниковых изображений
            </div>
          </div>

          <div className={styles.rightSide}>
            <nav className={styles.nav}>
              {links.map((link) => {
                const active = location.pathname === link.to;

                return (
                  <Link
                    key={link.id}
                    to={link.to}
                    className={active ? styles.navLinkActive : styles.navLink}
                  >
                    {link.title}
                  </Link>
                );
              })}
            </nav>

            <div className={styles.avatarWrapper}>
              <button
                className={styles.avatarBtn}
                onClick={() => setMenuOpen((value) => !value)}
                type="button"
                aria-label="Профиль"
              >
                {photoUrl ? (
                  <img
                    className={styles.avatarImg}
                    src={photoUrl}
                    alt="Аватар пользователя"
                  />
                ) : (
                  <div className={styles.avatarFallback}>{avatarLetter}</div>
                )}
              </button>

              {menuOpen && (
                <div className={styles.dropdown}>
                  {isAuth ? (
                    <>
                      <button
                        type="button"
                        className={styles.dropdownItem}
                        onClick={goToProfile}
                      >
                        Личный кабинет
                      </button>

                      <button
                        type="button"
                        className={styles.dropdownItem}
                        onClick={openLogoutModal}
                      >
                        Выход
                      </button>
                    </>
                  ) : (
                    <button
                      type="button"
                      className={styles.dropdownItem}
                      onClick={goToLogin}
                    >
                      Войти
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <ConfirmLogoutModal
        open={confirmOpen}
        onClose={() => setConfirmOpen(false)}
        onConfirm={handleConfirmLogout}
      />
    </>
  );
};

export default Header;