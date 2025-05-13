import React, { useState } from 'react';
import Slider from '@mui/material/Slider';

export default function DiscreteSlider({ onChange }) {
  const [sliderValue, setSliderValue] = useState(30);

  const handleChange = (event, newValue) => {
    setSliderValue(newValue);
    if (onChange) onChange(newValue); // Wert an Parent-Komponente weitergeben
  };

  return (
    <Slider
      value={sliderValue}
      onChange={handleChange}
      defaultValue={30}
      step={10}
      marks={[
        { value: 0, label: '0' },
        { value: 100, label: '100' }
      ]}
      min={0}
      max={100}
    />
  );
}