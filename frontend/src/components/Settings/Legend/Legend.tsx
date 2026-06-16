import s from "./Legend.module.scss";
import { getLegendByComposite } from "@/utils/composite";

interface Props {
  composite: string;
}

export const Legend = ({ composite }: Props) => {
  if (!composite) return null;

  return (
    <div className={s.legend}>
      <div className={s.title}>Легенда: {composite}</div>

      <img
        className={s.image}
        src={getLegendByComposite(composite)}
        alt={`Легенда ${composite}`}
      />
    </div>
  );
};