import styles from "./ConfirmLogoutModal.module.scss";

type Props = {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
};

export function ConfirmLogoutModal({ open, onClose, onConfirm }: Props) {
  if (!open) return null;

  return (
    <div className={styles.backdrop} onMouseDown={onClose}>
      <div className={styles.modal} onMouseDown={(e) => e.stopPropagation()}>
        <h2 className={styles.title}>Выход</h2>
        <p className={styles.text}>Вы уверены, что хотите выйти из учетной записи?</p>

        <div className={styles.actions}>
          <button className={styles.primary} onClick={onConfirm}>
            Выйти
          </button>
          <button className={styles.secondary} onClick={onClose}>
            Отменить
          </button>
        </div>
      </div>
    </div>
  );
}