import {Backdrop, CircularProgress} from "@mui/material";



export const Loading = () => {
    return(
        <Backdrop open>
            <CircularProgress color="inherit" />
        </Backdrop>
    )
}
