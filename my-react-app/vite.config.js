import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,  
    proxy: {
      // Proxy requests to /api to the Flask backend 
      '/api': {
        target: 'https://d15a-34-29-126-168.ngrok-free.app', // gnork url from colab notebook
        changeOrigin: true,
        secure: false,  // If HTTP or an insecure connection
      },
    },
  },
})
