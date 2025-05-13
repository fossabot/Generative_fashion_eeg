import React, { useState } from 'react';
import DiscreteSlider from './discreteslider';
import { Button } from '@mui/material';

export default function Image() {
    const [sliderValues, setSliderValues] = useState([0, 0, 0, 0]);

    const handleSliderChange = (index) => (newValue) => {
        const updatedValues = [...sliderValues];
        updatedValues[index] = newValue;
        setSliderValues(updatedValues);
    };

    const sendToBackend = async () => {
        try {
            const response = await fetch('http://localhost:5000/receive', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ value: sliderValues }),
                mode: 'cors',
            });
            const data = await response.json();
            console.log('Backend response:', data);
        } catch (error) {
            console.error('Error sending data:', error);
        }
        console.log('Sending data to backend:', sliderValues);
    };

    return (
        <div style={{
            height: '70vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
        }}>
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                gap: '2rem',
            }}>
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}>
                    <img
                        src="images/original.png"
                        alt="Centered"
                        style={{ maxWidth: '60%', height: 'auto', padding: '15px' }}
                    />
                    <DiscreteSlider onChange={handleSliderChange(0)} /> {/* Slider 1 */}
                </div>
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}>
                    <img
                        src="images/img_lila_6.5430.png"
                        alt="Centered"
                        style={{ maxWidth: '60%', height: 'auto', padding: '15px' }}
                    />
                    <DiscreteSlider onChange={handleSliderChange(1)} />
                </div>
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',git
                }}>
                    <img
                        src="images/img_white_6.3124.png"
                        alt="Centered"
                        style={{ maxWidth: '60%', height: 'auto', padding: '15px' }}
                    />
                    <DiscreteSlider onChange={handleSliderChange(2)} />
                </div>
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}>
                    <img
                        src="images/img_blue_6.7962.png"
                        alt="Centered"
                        style={{ maxWidth: '60%', height: 'auto', padding: '15px' }}
                    />
                    <DiscreteSlider onChange={handleSliderChange(3)} />
                </div>
            </div>
            <Button variant="contained" onClick={sendToBackend} style={{ marginTop: '20px' }}>
                Confirm
            </Button>
        </div>
    );
}