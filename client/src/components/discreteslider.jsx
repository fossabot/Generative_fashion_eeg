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
        { value: 10, label: '10' },
        { value: 20, label: '20' },
        { value: 30, label: '30' },
        { value: 40, label: '40' },
        { value: 50, label: '50' },
        { value: 60, label: '60' },
        { value: 70, label: '70' },
        { value: 80, label: '80' },
        { value: 90, label: '90' },
        { value: 100, label: '100' }
      ]}
      min={0}
      max={100}
    />
  );
}