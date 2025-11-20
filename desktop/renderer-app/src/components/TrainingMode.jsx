import React, { useState, useEffect } from 'react';
import { Chess } from 'chess.js';
import ChessBoardComponent from './ChessBoard';
import { getTrainingPosition, checkMove } from '../services/api';
import './TrainingMode.css';

export default function TrainingMode() {
  const [chess] = useState(new Chess());
  const [position, setPosition] = useState(chess.fen());
  const [trainingData, setTrainingData] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [difficulty, setDifficulty] = useState('intermediate');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadNewPosition();
  }, []);

  const loadNewPosition = async () => {
    try {
      setLoading(true);
      setFeedback(null);
      const response = await getTrainingPosition(difficulty, 'general');
      const data = response.data;
      setTrainingData(data);
      chess.load(data.fen);
      setPosition(chess.fen());
    } catch (err) {
      console.error('Failed to load training position:', err);
    } finally {
      setLoading(false);
    }
  };

  const onPieceDrop = async (sourceSquare, targetSquare) => {
    try {
      const move = chess.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: 'q'
      });

      if (move === null) return false;

      const moveUCI = `${sourceSquare}${targetSquare}`;
      const response = await checkMove(trainingData.fen, moveUCI);
      const result = response.data;

      setFeedback({
        correct: result.correct,
        explanation: result.explanation,
        bestMove: result.best_move,
        scoreLoss: result.score_loss
      });

      setPosition(chess.fen());
      return true;
    } catch (err) {
      console.error('Failed to check move:', err);
      return false;
    }
  };

  const handleNext = () => {
    chess.reset();
    loadNewPosition();
  };

  const handleDifficultyChange = (newDifficulty) => {
    setDifficulty(newDifficulty);
    chess.reset();
    loadNewPosition();
  };

  return (
    <div className="training-mode">
      <div className="training-header">
        <h2>Training Mode</h2>
        <div className="difficulty-selector">
          {['beginner', 'intermediate', 'advanced'].map(level => (
            <button
              key={level}
              className={difficulty === level ? 'active' : ''}
              onClick={() => handleDifficultyChange(level)}
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading position...</p>
        </div>
      ) : (
        <div className="training-content">
          <div className="board-section">
            <ChessBoardComponent
              position={position}
              onPieceDrop={onPieceDrop}
              boardWidth={450}
            />
          </div>

          <div className="training-panel">
            {trainingData && (
              <div className="objective">
                <h3>Objective</h3>
                <p>{trainingData.objective || 'Find the best move in this position.'}</p>
                {trainingData.hint && (
                  <div className="hint">
                    <strong>Hint:</strong> {trainingData.hint}
                  </div>
                )}
              </div>
            )}

            {feedback && (
              <div className={`feedback ${feedback.correct ? 'correct' : 'incorrect'}`}>
                <h3>{feedback.correct ? '✓ Correct!' : '✗ Not the best move'}</h3>
                <p>{feedback.explanation}</p>
                {!feedback.correct && (
                  <div className="best-move-hint">
                    <strong>Best move was:</strong> {feedback.bestMove}
                    <br />
                    <small>Score loss: {feedback.scoreLoss}cp</small>
                  </div>
                )}
                <button onClick={handleNext} className="next-button">
                  Next Position
                </button>
              </div>
            )}

            {!feedback && !loading && (
              <div className="instructions">
                <p>🎯 Make your move on the board</p>
                <p>💡 Take your time to find the best move</p>
                <p>📊 You'll get instant feedback</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
