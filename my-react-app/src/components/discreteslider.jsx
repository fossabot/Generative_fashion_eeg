import * as React from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';

function valuetext(value) {
  return `${value}°C`;
}


export default function DiscreteSlider() {
  return (
    <div style={{
      width: '80vh',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      <Slider
        aria-label="Temperature"
        defaultValue={30}
        getAriaValueText={valuetext}
        valueLabelDisplay="auto"
        shiftStep={30}
        step={10}
        marks
        min={0}
        max={100}
      />
      <Slider defaultValue={30} step={10} marks min={0} max={100} disabled />
    </div>
  );
}