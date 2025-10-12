import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import NotificationHub from './pages/NotificationHub';
import LiveVideo from './pages/LiveVideo';
import Login from './pages/Login';
import Create from './pages/Create';
import Store from './pages/Store';
import OurGoal from './pages/OurGoal';
import HowItWorks from './pages/HowItWorks';
import SetupGuide from './pages/SetupGuide';
import SafetyEthics from './pages/SafetyEthics';
import Maintenance from './pages/Maintenance';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/notifications" element={<NotificationHub />} />
          <Route path="/live-video" element={<LiveVideo />} />
          <Route path="/login" element={<Login />} />
          <Route path="/create" element={<Create />} />
          <Route path="/store" element={<Store />} />
          <Route path="/our-goal" element={<OurGoal />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/setup-guide" element={<SetupGuide />} />
          <Route path="/safety-ethics" element={<SafetyEthics />} />
          <Route path="/maintenance" element={<Maintenance />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
