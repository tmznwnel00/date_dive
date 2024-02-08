import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/user/Login';
import Signup from './pages/user/Signup';
import Home from './pages/Home';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path = "/" element={<Home />}></Route>
          <Route path = "/login" element={<Login />}></Route>
          <Route path = "/signup" element={<Signup />}></Route>
        </Routes>
      </Router>
     
    </div>
  );
}

export default App;
