import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import SignInPage from './pages/SignInPage'
import Admin_dash from './components/Admin_dash'

function App() {

  return (
    <>
      <h1>
        Asset Inventory Manager
      </h1>
      <Admin_dash />
    </>
  )
}

export default App
