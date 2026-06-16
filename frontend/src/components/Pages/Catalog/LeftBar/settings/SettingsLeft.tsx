import { settings } from '@/data/settings'
import s from './SettingsLeft.module.scss'
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { useAppDispatch, useAppSelector } from '@/hooks/hook';
import { useEffect, useState } from 'react';
import { setCompositeS, setSatelliteS } from '@/store/catalog/catalog-slice';


export const SettingsLeft = () => {

    const dispatch = useAppDispatch();
    const composite : string = useAppSelector(state => state.catalog).composite 
    const satellite : string = useAppSelector(state => state.catalog).sattelite 

    const [comp, setComp] = useState<string>('')
    const [satell, setSatell] = useState<string>('')

    useEffect(() => {
        setComp(composite);
    }, [composite]);

    useEffect(() => {
        setSatell(satellite);
    }, [satellite]);

    const handleChange = (e) => {
        if (e.target.name === '1') {
            setComp(e.target.value);
            dispatch(setCompositeS(e.target.value));
        } else if (e.target.name === '0') {
            setSatell(e.target.value);
            dispatch(setSatelliteS(e.target.value));
        }
    };


    return (
        <div className={s.settingsleft}>
            {settings.map((sett) => (
                <div className={s.setting}>
                    <p>{sett.name}</p>
                    <Box sx={{ minWidth: 120 }}>
                        <FormControl fullWidth>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                onChange={handleChange}
                                name={sett.type.toString()}
                                value={sett.type === 1 ? comp : satell}
                            >
                                {sett.setting.map((el) => (
                                    <MenuItem value={el.value}>{el.label}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Box>
                </div>
            ))}
            
        </div>
    )
}