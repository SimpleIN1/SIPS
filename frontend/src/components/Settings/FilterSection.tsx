import React, { useState, ReactNode } from "react";
import s from "./Settings.module.scss";

interface Props {
  title: string;
  children?: ReactNode;
}

const FilterSection = ({ title, children }: Props) => {

  const [open, setOpen] = useState(true);

  return (
    <div className={s.filterBlock}>

      <div
        className={s.filterHeader}
        onClick={() => setOpen(!open)}
      >

        <span>{title}</span>

        <span className={s.arrow}>
          {open ? "▴" : "▾"}
        </span>

      </div>

      {open && children && (
        <div className={s.filterContent}>
          {children}
        </div>
      )}

    </div>
  );
};

export default FilterSection;