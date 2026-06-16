
import {OverridableStringUnion} from "@mui/types";
import {SwitchPropsColorOverrides} from "@mui/material/Switch/Switch";
import {EUrls} from "@/enums/EUrls";

export interface IBorder{
    id: string,
    name: string,
    url: EUrls,
    color: OverridableStringUnion<
        'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning' | 'default',
        SwitchPropsColorOverrides
        >,
    checked: boolean
}