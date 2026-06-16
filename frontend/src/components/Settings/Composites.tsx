import { useState } from "react";
import FormControlLabel from "@mui/material/FormControlLabel";
import Switch from "@mui/material/Switch";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { toggleComposite } from "@/store/tile/tile-slice";
import { EComposite } from "@/enums/EComposite";
import s from "./Settings.module.scss";

const compositeDescriptions: Record<string, string> = {
  aot550:
    "Продукт, отражающий концентрацию аэрозольных частиц в атмосфере по ослаблению солнечного излучения на длине волны 550 нм. Используется для оценки качества воздуха и анализа дымовых шлейфов.",

  aotaps:
    "Продукт, отражающий концентрацию аэрозольных частиц в атмосфере с учетом поляризационных характеристик рассеянного излучения. Получен по алгоритму APS.",

  clphs:
    "Продукт, определяющий фазовое состояние облаков: жидкая, ледяная или смешанная фаза.",

  clmsk:
    "Маска облаков. Используется для определения облачных областей на спутниковом снимке.",

  clmsk2:
    "Улучшенная версия маски облаков с учетом дополнительных спектральных признаков.",

  frmsk:
    "Маска пожаров. Используется для выявления активных очагов возгорания.",

  vievi:
    "Индекс растительности EVI. Показывает состояние и плотность растительности.",

  vindvi:
    "Индекс растительности NDVI. Используется для оценки наличия и состояния растительной массы.",

  vlst:
    "Температура поверхности Земли с учетом данных о растительности.",

  vscmo:
    "Снежный покров за месяц. Используется для оценки устойчивых зон снежного покрова.",
};

interface CompositesProps {
  disabled?: boolean;
}

const Composites = ({ disabled = false }: CompositesProps) => {
  const dispatch = useAppDispatch();

  const composites = useAppSelector((state) => state.tile.composites) || [];
  const selectedComposite = useAppSelector((state) => state.tile.composite);

  const [hovered, setHovered] = useState<string | null>(null);

  if (disabled) {
    return (
      <div className={s.emptyText}>
        Сначала выберите спутник, дату и время съёмки
      </div>
    );
  }

  if (!composites || composites.length === 0) {
    return <div className={s.emptyText}>Композиты пока не загружены</div>;
  }

  return (
    <>
      <div className={s.compositesGrid}>
        {composites.map((item) => (
          <div
            key={item}
            className={s.compositeWrapper}
            onMouseEnter={() => setHovered(item)}
            onMouseLeave={() => setHovered(null)}
          >
            <FormControlLabel
              control={
                <Switch
                  checked={selectedComposite === (item as EComposite)}
                  onChange={() => dispatch(toggleComposite(item as EComposite))}
                />
              }
              label={item}
            />
          </div>
        ))}
      </div>

      {hovered && (
        <div className={s.compositeHint}>
          <div className={s.compositeHintTitle}>{hovered}</div>
          <div>{compositeDescriptions[hovered] || hovered}</div>
        </div>
      )}
    </>
  );
};

export default Composites;