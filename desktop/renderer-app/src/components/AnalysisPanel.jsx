import React from 'react';
import './AnalysisPanel.css';

export default function AnalysisPanel({ analysis, loading }) {
  if (loading) {
    return (
      <div className="analysis-panel">
        <div className="spinner"></div>
        <p>Analyzing position...</p>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="analysis-panel">
        <p className="placeholder">No analysis yet. Analyze a position or game to see results.</p>
      </div>
    );
  }

  const { score, best_move, evaluation, move_analysis } = analysis;

  return (
    <div className="analysis-panel">
      <h3>Analysis</h3>

      <div className="eval-section">
        <div className="eval-bar">
          <div
            className="eval-fill"
            style={{
              width: `${Math.min(Math.max((score + 500) / 10, 0), 100)}%`,
              background: score > 100 ? '#4CAF50' : score < -100 ? '#f44336' : '#FFC107'
            }}
          ></div>
        </div>
        <div className="eval-score">
          Evaluation: {score > 0 ? '+' : ''}{(score / 100).toFixed(2)}
        </div>
      </div>

      {best_move && (
        <div className="best-move">
          <strong>Best Move:</strong> {best_move}
        </div>
      )}

      {evaluation && (
        <div className="evaluation-text">
          <strong>Position:</strong> {evaluation}
        </div>
      )}

      {move_analysis && move_analysis.length > 0 && (
        <div className="moves-list">
          <h4>Move Analysis</h4>
          <div className="moves-container">
            {move_analysis.slice(0, 10).map((move, index) => (
              <div key={index} className={`move-item ${move.classification}`}>
                <span className="move-number">{move.move_number}.</span>
                <span className="move-san">{move.move}</span>
                <span className="move-eval">{move.score_after}cp</span>
                <span className="move-class">{move.classification}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
