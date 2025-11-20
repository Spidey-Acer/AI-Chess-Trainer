import React, { useState, useEffect } from 'react';
import { listGames } from '../services/api';
import './GameList.css';

export default function GameList({ onSelectGame }) {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadGames();
  }, []);

  const loadGames = async () => {
    try {
      setLoading(true);
      const response = await listGames(50, 0);
      setGames(response.data.games || []);
      setError(null);
    } catch (err) {
      setError('Failed to load games');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="game-list">
        <div className="spinner"></div>
        <p>Loading games...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="game-list">
        <div className="error">{error}</div>
        <button onClick={loadGames}>Retry</button>
      </div>
    );
  }

  if (games.length === 0) {
    return (
      <div className="game-list">
        <div className="placeholder">
          <p>No games yet. Import a PGN file to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="game-list">
      <h3>Your Games</h3>
      <div className="games-container">
        {games.map((game) => (
          <div
            key={game.id}
            className="game-item"
            onClick={() => onSelectGame(game)}
          >
            <div className="game-header">
              <span className="player white">{game.white_player}</span>
              <span className="vs">vs</span>
              <span className="player black">{game.black_player}</span>
            </div>
            <div className="game-meta">
              <span className="result">{game.result}</span>
              <span className="date">{game.date}</span>
            </div>
            {game.white_accuracy && (
              <div className="accuracy">
                <span>White: {game.white_accuracy}%</span>
                <span>Black: {game.black_accuracy}%</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
