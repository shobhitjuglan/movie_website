import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './css/App.css'
import MovieCard from './components/MovieCard'
import Home from './pages/Home'
import { Routes, Route } from 'react-router-dom'
import Favorites from './pages/Favorites'
import Navbar from './components/Navbar'
import { MovieProvider } from './contexts/MovieContext'

function App() {
  const movieNumber = 1

  return (
    <div>
      <MovieProvider>
        <Navbar/>
        <main className='main-content'>
          <Routes>
            <Route path="/" element={<Home />}></Route>
            <Route path="/favorites" element={<Favorites />}></Route>
          </Routes>
        </main>
      </MovieProvider>
    </div>
  );
}

function Text({text}) {
  return(
    <>
      <div>{text}</div>
    </>
  )
}

export default App
