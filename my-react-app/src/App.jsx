import { useEffect, useState } from 'react'
import DiscreteSlider from './components/discreteslider'
import Image from './components/image_component'
import { Button } from '@mui/material'
import Dashboard from './dashboard'
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';




function Home() {
  const [ currentTime, setTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json().then(data => {
    setTime(data.time);
    }))
  }, []);
  
  return (
    <div style={{
      paddingTop:'4rem',
      display: 'flex', 
      flexDirection: 'column', //!!!!
      alignItems: 'center',
      padding: '1rem',
      height: '100vh', 
      fontFamily: 'Avenir',
      fontWeight: 'bold',
      paddingRight: '4rem',
      paddingLeft: '4rem',
    }}>
      <div style={{display: 'flex', flexDirection: 'column',alignItems: 'center',justifyContent: 'center',
      
      paddingBottom: '2rem',
      height: '20vh', 
    }}>
      <h1>Generative Fashion</h1> 
      </div>
      <p>The current time is {currentTime} </p>
      <Image></Image>
    </div>

  )
}

function App() {
  
  
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App

