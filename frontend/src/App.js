import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Register from './components/Register';
import Login from './components/Login';

function App() {
  return (
    <div>
      <Router>
        <div>
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route exact path="/register" element={<Register />} />
            <Route exact path="/login" element={<Login />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
