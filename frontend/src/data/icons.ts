import {Icon} from "leaflet";

export const icons = () => {
    const customIcon = new Icon({
        iconUrl: require("../assets/icons/blueIcon.png"),
        iconSize: [60, 60]
    });

    const rulerIcon = new Icon({
        iconUrl: require("../assets/icons/svg/dot-small-svgrepo-com.svg"),
        iconSize:[50, 50]
    })
    const emptyIcon = new Icon({
        iconUrl: require("../assets/icons/emptyIcon.png"),
        iconSize:[40, 40]
    })
    const settlementIcon = new Icon({
        iconUrl: require("../assets/icons/svg/method-draw-image (1).svg"),
        iconSize:[20, 20]
    })

    return {customIcon, rulerIcon, emptyIcon, settlementIcon}
}