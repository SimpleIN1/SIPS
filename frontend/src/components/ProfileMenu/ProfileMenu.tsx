import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { logout } from "@/store/user/user-slice"; // твой reducer logout()

export function ProfileMenu() {
  const [open, setOpen] = useState(false);
  const [confirmOpen, setConfirmOpen] = useState(false);

  const isAuth = useAppSelector((s) => s.user.isAuth);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const onLogout = () => {
    dispatch(logout());          // чистим localStorage + state
    setConfirmOpen(false);
    setOpen(false);
    navigate("/");               // или /authorization — как тебе нужно
  };

  return (
    <div style={{ position: "relative" }}>
      <button onClick={() => setOpen(v => !v)} aria-label="Профиль">
        Л
      </button>

      {open && (
        <div style={{ position: "absolute", right: 0, top: "110%", width: 180 }}>
          {!isAuth ? (
            <button onClick={() => { setOpen(false); navigate("/authorization"); }}>
              Авторизация
            </button>
          ) : (
            <>
              <button onClick={() => { setOpen(false); navigate("/profile"); }}>
                Личный кабинет
              </button>
              <button onClick={() => { setOpen(false); setConfirmOpen(true); }}>
                Выход
              </button>
            </>
          )}
        </div>
      )}

      {confirmOpen && (
        <div /* тут твоя модалка как на макете */>
          <div>Вы уверены, что хотите выйти из учетной записи?</div>
          <button onClick={onLogout}>Выйти</button>
          <button onClick={() => setConfirmOpen(false)}>Отменить</button>
        </div>
      )}
    </div>
  );
}