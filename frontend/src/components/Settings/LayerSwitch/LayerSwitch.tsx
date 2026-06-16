import React from "react";
import { Radio, RadioGroup } from "@mui/material";
import FormControlLabel from "@mui/material/FormControlLabel";
import { FormControl } from "@mui/base";
import s from "@/components/Settings/Settings.module.scss";
import { layers } from "@/data/layers";
import { useAppDispatch, useAppSelector } from "@/hooks/hook";
import { setLayer } from "@/store/map/map-slice";

const LayerSwitch = () => {
  const dispatch = useAppDispatch();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setLayer((e.target as HTMLInputElement).value));
  };
  const layer = useAppSelector((state) => state.map).layer;

  return (
    <FormControl>
      <p className={s.text}>Выбор слоя</p>
      <RadioGroup
        aria-labelledby="demo-radio-buttons-group-label"
        defaultValue={layer}
        name="radio-buttons-group"
        onChange={handleChange}
        
      >
        {layers.map((layer, index) => (
          <FormControlLabel    
            key={index}
            value={layer.url}
            control={<Radio size="small"/>}
            label={layer.name}
          />
        ))}
      </RadioGroup>
    </FormControl>
  );
};

export default LayerSwitch;
