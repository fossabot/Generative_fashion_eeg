import { useEffect, useState } from 'react'
import DiscreteSlider from '../components/discreteslider'
import Image from '../components/image_component'
  
function App() {
  const [message, setMessage] = useState('Loading...')

  useEffect(() => {
    fetch('/api/hello') //  proxy to ngrok
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => setMessage('Error: ' + err.message))
  }, [])

  return (
    <div style={{ fontFamily: 'Arial', padding: '2rem' }}>
      <h1>Generative Fashion using EEG </h1> 
      <Image></Image>
      <DiscreteSlider></DiscreteSlider>
    </div>
  )
}

export default App
