import { useEffect, useState } from 'react'
import DiscreteSlider from './components/discreteslider'
import Image from './components/image_component'
import { Button } from '@mui/material'
import Dashboard from './dashboard'
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';




function Home() {
  const [message, setMessage] = useState('Loading...')

  useEffect(() => {
    fetch('/api/hello') //  proxy to ngrok
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => setMessage('Error: ' + err.message))
  }, [])

  return (
    <div style={{
      display: 'flex', 
      flexDirection: 'column', //!!!!
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'Avenir',
      fontWeight: 'bold',
      padding: '2rem',
      height: '100vh', 
    }}>
      <h1>Generative Fashion Using EEG Data</h1>
      <Image></Image>
      <DiscreteSlider></DiscreteSlider>
      <Button variant="contained">Confirm</Button>
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

