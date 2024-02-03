import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path = "/login" element={<Login />}></Route>
          <Route path = "/signup" element={<Signup />}></Route>
        </Routes>
      </Router>
     
    </div>
  );
}

export default App;
