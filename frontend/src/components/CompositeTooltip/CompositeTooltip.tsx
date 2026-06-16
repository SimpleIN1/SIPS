import "./CompositeTooltip.scss"

const descriptions = {
  vlst: "Индекс растительности с температурой поверхности",
  aot550: "Оптическая толщина аэрозоля",
  vscmo: "Маска облачности",
  clmsk: "Облачная маска",
  clmsk2: "Расширенная облачная маска",
  aotaps: "Аэрозольный продукт APS",
  frmsk: "Маска пожаров",
  clphs: "Фаза облаков",
  vievi: "Индекс растительности EVI",
  vindvi: "Индекс NDVI"
}

const CompositeTooltip = ({type}) => {

  return (
    <div className="tooltip">
      {descriptions[type]}
    </div>
  )
}

export default CompositeTooltip