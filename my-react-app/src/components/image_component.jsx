import React, { useState } from 'react';
import DiscreteSlider from './discreteslider';
import { Button } from '@mui/material';

export default function Image() {
    
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
                    <DiscreteSlider /> 
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
                    <DiscreteSlider/>
                </div>
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}>
                    <img
                        src="images/img_white_6.3124.png"
                        alt="Centered"
                        style={{ maxWidth: '60%', height: 'auto', padding: '15px' }}
                    />
                    <DiscreteSlider />
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
                    <DiscreteSlider />
                </div>
            </div>
            <Button variant="contained" style={{ marginTop: '20px' }}>
                Confirm
            </Button>
        </div>
    );
}