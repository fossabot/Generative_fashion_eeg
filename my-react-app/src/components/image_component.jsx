import React from 'react';

export default function Image() {
        return (
        <div style={{
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        }}>
        <img 
            src="images/original.png" 
            alt="Centered" 
            style={{ maxWidth: '35%', height: 'auto' }} 
        />
        </div>
    );
}
