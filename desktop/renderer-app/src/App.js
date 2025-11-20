import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import AnalyzePage from './pages/AnalyzePage';
import TrainingMode from './components/TrainingMode';
import StatsDisplay from './components/StatsDisplay';
import GameList from './components/GameList';
import './App.css';

function App() {
  const [selectedGame, setSelectedGame] = useState(null);

  return (
    <Router>
      <div className="app">
        <nav className="sidebar">
          <div className="app-title">
            <h1>♟️</h1>
            <h2>AI Chess Trainer</h2>
          </div>

          <div className="nav-links">
            <Link to="/analyze" className="nav-link">
              <span className="icon">📊</span>
              <span>Analyze</span>
            </Link>
            <Link to="/train" className="nav-link">
              <span className="icon">🎯</span>
              <span>Train</span>
            </Link>
            <Link to="/games" className="nav-link">
              <span className="icon">📚</span>
              <span>Games</span>
            </Link>
            <Link to="/stats" className="nav-link">
              <span className="icon">📈</span>
              <span>Statistics</span>
            </Link>
          </div>

          <div className="sidebar-footer">
            <div className="status-indicator">
              <span className="status-dot"></span>
              <span>Backend Ready</span>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/analyze" replace />} />
            <Route path="/analyze" element={<AnalyzePage />} />
            <Route path="/train" element={<TrainingMode />} />
            <Route path="/games" element={<GameList onSelectGame={setSelectedGame} />} />
            <Route path="/stats" element={<StatsDisplay />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
