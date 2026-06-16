import { useState, ReactNode } from "react";
import s from "./Settings.module.scss";

interface Props {
  title: string;
  children: ReactNode;
}

const Accordion = ({ title, children }: Props) => {
  const [open, setOpen] = useState(true);

  return (
    <div className={s.filterCard}>
      <div className={s.filterHeader} onClick={() => setOpen(!open)}>
        <span>{title}</span>
        <span className={s.arrow}>{open ? "▴" : "▾"}</span>
      </div>

      {open && <div className={s.filterBody}>{children}</div>}
    </div>
  );
};

export default Accordion;