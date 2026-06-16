import s from './BackArrow.module.scss'
import {useNavigate} from "react-router-dom";




export const BackArrow= () => {
    let navigate = useNavigate();

    const handleClick = () => {
        navigate(-1)
    }

    return(
        <button onClick={handleClick}  className={s.arrow}>
            <svg width="800px" height="800px" viewBox="0 0 1024 1024" className="icon" version="1.1"
                 xmlns="http://www.w3.org/2000/svg" fill="#000000">
                <g id="SVGRepo_bgCarrier" strokeWidth="0"/>
                <g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"/>
                <g id="SVGRepo_iconCarrier">
                    <path d="M768 903.232l-50.432 56.768L256 512l461.568-448 50.432 56.768L364.928 512z"
                          fill="#ffffff"/>
                </g>
            </svg>
        </button>
    )
}