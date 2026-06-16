import {createSlice} from "@reduxjs/toolkit";
import {RulerState} from "@/store/ruler/ruler-state";


const initialState = {
    isRulerActive: false,
    rulerMarkers: [],
    rulerMarkersPos: [],
}as RulerState


const rulerSlice = createSlice({
    name: 'ruler',
    initialState,
    reducers:{
        changeIsRulerActive(state){
            state.isRulerActive = !state.isRulerActive
        },
        addRulerMarker(state, action){
            state.rulerMarkers.push(action.payload)
        },
        addRulerMarkerPos(state, action){
            state.rulerMarkersPos.push(action.payload)
        },
        removeRulerMarkers(state){
            state.rulerMarkers = []
            state.rulerMarkersPos = []
        },
    },

})

export const {
    changeIsRulerActive,
    addRulerMarker,
    addRulerMarkerPos,
    removeRulerMarkers
} = rulerSlice.actions
export default rulerSlice.reducer