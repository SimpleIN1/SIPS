import React from 'react';
import s from './Cursor.module.scss'
import {useAppSelector} from "@/hooks/hook";



const Cursor = () => {
    const cursorPosition = useAppSelector(state => state.cursor).cursorPosition
    return (
        <div className={s.cursor} style={{ left: cursorPosition.x - 25, top: cursorPosition.y - 25 }}>
            <svg width="50px" height="50px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <g id="SVGRepo_bgCarrier" strokeWidth="0"/>
                <g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"/>
                <g id="SVGRepo_iconCarrier"> <path d="M12 9.5C13.3807 9.5 14.5 10.6193 14.5 12C14.5 13.3807 13.3807 14.5 12 14.5C10.6193 14.5 9.5 13.3807 9.5 12C9.5 10.6193 10.6193 9.5 12 9.5Z" fill="#ff0000"/> </g>
            </svg>
        </div>
    );
};

export default Cursor;