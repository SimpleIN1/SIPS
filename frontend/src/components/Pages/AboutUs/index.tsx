import { CSSProperties, useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import styles from "./AboutUs.module.scss";

type ProductCard = {
  key: string;
  title: string;
  category: string;
  accent: string;
  text: string;
};

const DOTS_COUNT = 7;

const AboutUs = () => {
  const cards: ProductCard[] = useMemo(
    () => [
      {
        key: "aot550",
        title: "AOT550",
        category: "Аэрозоли",
        accent: "#2563eb",
        text: "Продукт, отражающий концентрацию аэрозольных частиц в атмосфере по ослаблению солнечного излучения на длине волны 550 нм, используемый для оценки качества воздуха и анализа дымовых шлейфов.",
      },
      {
        key: "aotaps",
        title: "AOTAPS",
        category: "Аэрозоли",
        accent: "#1d4ed8",
        text: "Продукт, отражающий концентрацию аэрозольных частиц в атмосфере по ослаблению солнечного излучения на длине волны 550 нм, учитывающий поляризационные характеристики рассеянного излучения, полученный по алгоритму APS.",
      },
      {
        key: "aps",
        title: "APS",
        category: "Поляриметрия",
        accent: "#4f46e5",
        text: "Алгоритм, учитывающий поляризацию при определении оптической толщины аэрозоля.",
      },
      {
        key: "clphs",
        title: "CLPHS",
        category: "Фаза облаков",
        accent: "#64748b",
        text: "Продукт, определяющий фазовое состояние облаков (жидкая, ледяная, смешанная) на основе теплового излучения в инфракрасных каналах.",
      },
      {
        key: "clmsk",
        title: "CLMSK",
        category: "Маска облачности",
        accent: "#38bdf8",
        text: "Продукт, классифицирующий пиксели по наличию облаков на основе данных каналов M1–M16 радиометра VIIRS. Используется как фильтр для исключения облачных зон при анализе поверхности.",
      },
      {
        key: "clmsk2",
        title: "CLMSK2",
        category: "Маска облачности",
        accent: "#0ea5e9",
        text: "Продукт, представляющий улучшенную версию clmsk с учётом фазы облаков и дополнительных спектральных признаков.",
      },
      {
        key: "frmsk",
        title: "FRMSK",
        category: "Пожары",
        accent: "#ef4444",
        text: "Продукт, выявляющий активные очаги пожаров по аномально высокой яркостной температуре в инфракрасном диапазоне.",
      },
      {
        key: "vievi",
        title: "VIEVI",
        category: "Растительность",
        accent: "#22c55e",
        text: "Продукт, который корректирует атмосферные эффекты и насыщение сигнала в густой растительности, обеспечивая повышенную чувствительность.",
      },
      {
        key: "evi",
        title: "EVI",
        category: "Индекс растительности",
        accent: "#15803d",
        text: "Вегетационный индекс, который используется для оценки здоровья и плотности растительности, разработанный для улучшения показателей, получаемых с помощью Normalized Difference Vegetation Index.",
      },
      {
        key: "vindvi",
        title: "VINDVI",
        category: "Растительность",
        accent: "#16a34a",
        text: "Продукт, вычисляемый как нормализованная разность отражений в ближнем инфракрасном и красном спектральных диапазонах.",
      },
      {
        key: "ndvi",
        title: "NDVI",
        category: "Индекс растительности",
        accent: "#65a30d",
        text: "Вегетационный индекс, определяющий наличие растительной массы на некотором участке поверхности земли.",
      },
      {
        key: "vlst",
        title: "VLST",
        category: "Температура поверхности",
        accent: "#f97316",
        text: "Продукт, объединяющий вегетационный индекс с данными о температуре поверхности Земли.",
      },
      {
        key: "lst",
        title: "LST",
        category: "Температура поверхности",
        accent: "#ea580c",
        text: "Температура поверхности Земли, измеряемая спутниками с помощью теплового инфракрасного излучения.",
      },
      {
        key: "vscmo",
        title: "VSCMO",
        category: "Снежный покров",
        accent: "#0284c7",
        text: "Продукт, формирующийся путём агрегации ежедневных наблюдений за месяц для определения устойчивых зон снега.",
      },
    ],
    []
  );

  const trackRef = useRef<HTMLDivElement | null>(null);
  const [active, setActive] = useState(0);

  const activeDot = Math.round(
    (active / Math.max(cards.length - 1, 1)) * (DOTS_COUNT - 1)
  );

  const getCards = () => {
    const track = trackRef.current;

    if (!track) {
      return [];
    }

    return Array.from(track.querySelectorAll<HTMLElement>(`[data-card="1"]`));
  };

  const scrollToIndex = (index: number) => {
    const track = trackRef.current;
    const items = getCards();

    if (!track || !items.length) {
      return;
    }

    const safeIndex = Math.max(0, Math.min(index, items.length - 1));
    const target = items[safeIndex];

    track.scrollTo({
      left: target.offsetLeft - track.offsetLeft,
      behavior: "smooth",
    });

    setActive(safeIndex);
  };

  useEffect(() => {
    const track = trackRef.current;

    if (!track) {
      return;
    }

    const handleScroll = () => {
      const items = getCards();

      if (!items.length) {
        return;
      }

      let bestIndex = 0;
      let bestDistance = Number.POSITIVE_INFINITY;

      items.forEach((item, index) => {
        const distance = Math.abs(
          item.offsetLeft - track.offsetLeft - track.scrollLeft
        );

        if (distance < bestDistance) {
          bestDistance = distance;
          bestIndex = index;
        }
      });

      setActive(bestIndex);
    };

    handleScroll();

    track.addEventListener("scroll", handleScroll, { passive: true });
    window.addEventListener("resize", handleScroll);

    return () => {
      track.removeEventListener("scroll", handleScroll);
      window.removeEventListener("resize", handleScroll);
    };
  }, []);

  useEffect(() => {
    const timer = window.setInterval(() => {
      const track = trackRef.current;

      if (!track) {
        return;
      }

      const rect = track.getBoundingClientRect();
      const isVisible = rect.top < window.innerHeight && rect.bottom > 0;

      if (!isVisible) {
        return;
      }

      const nextIndex = active >= cards.length - 1 ? 0 : active + 1;

      scrollToIndex(nextIndex);
    }, 3000);

    return () => window.clearInterval(timer);
  }, [active, cards.length]);

  return (
    <div className={styles.root}>
      <section className={styles.hero}>
        <div className={styles.heroLeft}>
          <p className={styles.heroText}>
            Разрабатывайте, анализируйте и открывайте новое с данными VIIRS,
            превращая сложные спутниковые данные в ясные и информативные
            визуализации.
          </p>
        </div>

        <div className={styles.heroRight}>
          <h1 className={styles.heroTitle}>
            РАСЧЕТ И
            <br />
            ВИЗУАЛИЗАЦИЯ
            <br />
            ДАННЫХ
          </h1>
        </div>
      </section>

      <section className={styles.features}>
        <h2 className={styles.featuresTitle}>ВОЗМОЖНОСТИ SIPS</h2>

        <div className={styles.featuresGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureNumber}>01</div>
            <div className={styles.featureTitle}>Интерактивная карта</div>
            <div className={styles.featureText}>
              Просмотр спутниковых продуктов на карте с возможностью выбора
              подложки, масштаба и дополнительных географических слоёв.
            </div>
          </div>

          <div className={styles.featureCard}>
            <div className={styles.featureNumber}>02</div>
            <div className={styles.featureTitle}>Выбор данных</div>
            <div className={styles.featureText}>
              Выбор спутника, даты, времени съёмки и композита для отображения
              нужного спутникового продукта.
            </div>
          </div>

          <div className={styles.featureCard}>
            <div className={styles.featureNumber}>03</div>
            <div className={styles.featureTitle}>Скачивание продуктов</div>
            <div className={styles.featureText}>
              Для авторизованного пользователя доступна загрузка выбранного
              продукта для дальнейшей работы и анализа.
            </div>
          </div>
        </div>
      </section>

      <section className={styles.products}>
        <h2 className={styles.sectionBigTitle}>ПРЕДОСТАВЛЯЕМЫЕ ПРОДУКТЫ</h2>

        <div className={styles.track} ref={trackRef}>
          {cards.map((card) => (
            <div
              key={card.key}
              className={styles.card}
              data-card="1"
              style={{ "--accent": card.accent } as CSSProperties}
            >
              <div className={styles.cardAccent} />

              <div className={styles.cardHeader}>
                <div className={styles.cardTitle}>{card.title}</div>
                <div className={styles.cardCategory}>{card.category}</div>
              </div>

              <div className={styles.cardText}>{card.text}</div>
            </div>
          ))}
        </div>

        <div className={styles.dots}>
          {Array.from({ length: DOTS_COUNT }).map((_, index) => (
            <button
              key={index}
              type="button"
              className={activeDot === index ? styles.dotActive : styles.dot}
              aria-label={`Перейти к группе продуктов ${index + 1}`}
              onClick={(event) => {
                event.preventDefault();
                event.stopPropagation();

                const items = getCards();

                if (!items.length) {
                  return;
                }

                const targetIndex = Math.floor(
                  (index / (DOTS_COUNT - 1)) * (items.length - 1)
                );

                scrollToIndex(targetIndex);
              }}
            />
          ))}
        </div>
      </section>

      <section className={styles.guide}>
        <h2 className={styles.sectionBigTitle}>РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ</h2>

        <div className={styles.steps}>
          <div className={styles.step}>
            <div className={styles.stepNum}>1</div>
            <div className={styles.stepText}>
              Выберите тип карты для визуализации и при необходимости добавьте
              дополнительные параметры, такие как границы регионов, заповедники
              или населённые пункты.
            </div>
          </div>

          <div className={styles.step}>
            <div className={styles.stepNum}>2</div>
            <div className={styles.stepText}>
              Выберите спутник для получения данных. После этого откроется окно
              выбора даты наблюдения.
            </div>
          </div>

          <div className={styles.step}>
            <div className={styles.stepNum}>3</div>
            <div className={styles.stepText}>
              Укажите интересующую дату и выберите продукт, который хотите
              просмотреть. Выбранный продукт отобразится на карте.
            </div>
          </div>

          <div className={styles.step}>
            <div className={styles.stepNum}>4</div>
            <div className={styles.stepText}>
              Сохраните нужный снимок на локальный компьютер с помощью функции
              экспорта или измените параметры и выберите другой продукт для
              загрузки.
            </div>
          </div>
        </div>

        <Link to="/" className={styles.toMapBtn}>
          НА КАРТУ
        </Link>
      </section>

      <footer className={styles.footer}>
        <div className={styles.footerInner}>
          <div className={styles.footerCol}>
            <div className={styles.footerTitle}>Адрес</div>
            <div>630090, Россия, г. Новосибирск</div>
            <div>ул. Лавреньева 6</div>

            <div className={styles.footerTitle} style={{ marginTop: 12 }}>
              Телефон
            </div>
            <div>+7(383) 330-61-50</div>

            <div className={styles.footerTitle} style={{ marginTop: 12 }}>
              E-mail
            </div>
            <div>ict@ict.nsc.ru</div>
          </div>

          <div className={styles.footerCol}>
            <div className={styles.footerTitle}>
              Федеральный исследовательский центр информационных и
              вычислительных технологий (ФИЦ ИВТ)
            </div>

            <a
              href="http://www.ict.nsc.ru/"
              target="_blank"
              rel="noopener noreferrer"
              className={styles.footerLink}
            >
              www.ict.nsc.ru
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default AboutUs;