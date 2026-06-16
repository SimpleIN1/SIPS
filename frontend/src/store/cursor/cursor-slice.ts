import {createSlice} from "@reduxjs/toolkit";
import {CursorState} from "@/store/cursor/cursor-state";


const initialState = {
    mousePos: { lat: 0, lng: 0 },
    cursorPosition:{
        y: null,
        x: null
    },
    isActive: false
}as CursorState


const cursorSlice = createSlice({
    name: 'cursor',
    initialState,
    reducers:{
        changeCursorActive(state){
            state.isActive = !state.isActive
        },
        setCursorPosition(state, action){
            state.cursorPosition = action.payload
        },
        setMousePos(state, action){
            state.mousePos.lat = action.payload.lat
            state.mousePos.lng = action.payload.lng
        },
    },

})

export const {
    changeCursorActive,
    setCursorPosition,
    setMousePos
} = cursorSlice.actions
export default cursorSlice.reducer