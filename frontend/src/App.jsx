import React from "react"
import { BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import Landing from "./pages/Landing"
import Visualise from "./pages/Visualise"

function Logout(){
  localStorage.clear()
  return <Navigate to = "/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path = "/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        /> 
        <Route path ="/login" element ={<Login />}></Route>
        <Route path ="/logout" element ={<Logout />}></Route>
        <Route path ="/register" element ={<RegisterAndLogout />}></Route>
        <Route path ="*" element ={<NotFound />}></Route>
        <Route path ="/landing" element ={<Landing />}></Route>
                <Route path ="/visualise" element ={<Visualise />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
