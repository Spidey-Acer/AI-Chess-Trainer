import React, { useState } from 'react';
import { Chess } from 'chess.js';
import ChessBoardComponent from '../components/ChessBoard';
import AnalysisPanel from '../components/AnalysisPanel';
import { analyzeGame, analyzePosition } from '../services/api';
import './AnalyzePage.css';

export default function AnalyzePage() {
  const [chess] = useState(new Chess());
  const [position, setPosition] = useState(chess.fen());
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pgnText, setPgnText] = useState('');
  const [mode, setMode] = useState('position'); // 'position' or 'game'

  const handleAnalyzePosition = async () => {
    try {
      setLoading(true);
      const response = await analyzePosition(position, 20);
      setAnalysis(response.data);
    } catch (err) {
      console.error('Failed to analyze position:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeGame = async () => {
    try {
      setLoading(true);
      const response = await analyzeGame(pgnText, 20, false);
      setAnalysis(response.data);
    } catch (err) {
      console.error('Failed to analyze game:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenFile = async () => {
    if (window.electronAPI) {
      const result = await window.electronAPI.openFileDialog();
      if (result) {
        setPgnText(result.content);
      }
    }
  };

  const handleReset = () => {
    chess.reset();
    setPosition(chess.fen());
    setAnalysis(null);
    setPgnText('');
  };

  return (
    <div className="analyze-page">
      <div className="analyze-header">
        <h2>Analyze</h2>
        <div className="mode-selector">
          <button
            className={mode === 'position' ? 'active' : ''}
            onClick={() => setMode('position')}
          >
            Position
          </button>
          <button
            className={mode === 'game' ? 'active' : ''}
            onClick={() => setMode('game')}
          >
            Game
          </button>
        </div>
      </div>

      {mode === 'position' ? (
        <div className="analyze-content">
          <div className="board-section">
            <ChessBoardComponent
              position={position}
              boardWidth={450}
            />
            <div className="position-controls">
              <button onClick={handleAnalyzePosition} disabled={loading}>
                {loading ? 'Analyzing...' : 'Analyze Position'}
              </button>
              <button onClick={handleReset}>Reset</button>
            </div>
          </div>
          <div className="analysis-section">
            <AnalysisPanel analysis={analysis} loading={loading} />
          </div>
        </div>
      ) : (
        <div className="analyze-content">
          <div className="pgn-section">
            <textarea
              value={pgnText}
              onChange={(e) => setPgnText(e.target.value)}
              placeholder="Paste PGN here or open a file..."
              rows={15}
            />
            <div className="pgn-controls">
              <button onClick={handleOpenFile}>Open PGN File</button>
              <button onClick={handleAnalyzeGame} disabled={loading || !pgnText}>
                {loading ? 'Analyzing...' : 'Analyze Game'}
              </button>
              <button onClick={handleReset}>Clear</button>
            </div>
          </div>
          <div className="analysis-section">
            <AnalysisPanel analysis={analysis} loading={loading} />
          </div>
        </div>
      )}
    </div>
  );
}
