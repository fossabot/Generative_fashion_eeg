import React, { useState, useEffect, use } from 'react';
import ImageRatingComponent from './components/image_ratings';
function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("http://127.0.0.1:5000/members")
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error("Error fetching data:", error));
    setData(data);
    console.log(data);

  }, []);

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column', //!!!!
      alignItems: 'center',
      height: '100vh',
      fontWeight: 'bold',

    }}>
      <div style={{ paddingBottom: '0rem', fontFamily: 'Avenir', paddingTop: '4rem', fontSize: '1rem' }}>
        <h1>Generative Fashion</h1>
      </div>
      <div style={{
       paddingRight: '2rem', paddingLeft: '2rem',
      }}>
        <ImageRatingComponent></ImageRatingComponent>
      </div>
    </div>
  );
}

export default App;
