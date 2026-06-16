
export const convertCoords = (latlngcoord: number):string => {
    const degree = Math.trunc(latlngcoord)
    const fractionsminute = (latlngcoord - degree) * 60
    const minute = Math.trunc(fractionsminute)
    const fractionssecond = fractionsminute - minute
    const second = Number((fractionssecond * 60).toFixed(2))

    return Math.abs(degree) + '°' + Math.abs(minute) + "'" + Math.abs(second) + '"'
}