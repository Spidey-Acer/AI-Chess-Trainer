import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getStats } from '../services/api';
import './StatsDisplay.css';

export default function StatsDisplay() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const response = await getStats();
      setStats(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="stats-display">
        <div className="spinner"></div>
        <p>Loading statistics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="stats-display">
        <div className="error">{error}</div>
        <button onClick={loadStats}>Retry</button>
      </div>
    );
  }

  if (!stats || stats.total_games === 0) {
    return (
      <div className="stats-display">
        <div className="placeholder">
          <p>No statistics yet. Analyze some games to see your progress!</p>
        </div>
      </div>
    );
  }

  const { total_games, avg_accuracy, total_blunders, total_mistakes, improvement_trend, opening_performance } = stats;

  return (
    <div className="stats-display">
      <h2>Your Statistics</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{total_games}</div>
          <div className="stat-label">Total Games</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{avg_accuracy?.toFixed(1)}%</div>
          <div className="stat-label">Average Accuracy</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{total_blunders}</div>
          <div className="stat-label">Total Blunders</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{total_mistakes}</div>
          <div className="stat-label">Total Mistakes</div>
        </div>
      </div>

      {improvement_trend && improvement_trend.length > 0 && (
        <div className="chart-section">
          <h3>Accuracy Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={improvement_trend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="date" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip
                contentStyle={{ background: '#1e1e1e', border: '1px solid #667eea' }}
                labelStyle={{ color: '#fff' }}
              />
              <Legend wrapperStyle={{ color: '#fff' }} />
              <Line type="monotone" dataKey="accuracy" stroke="#667eea" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {opening_performance && Object.keys(opening_performance).length > 0 && (
        <div className="chart-section">
          <h3>Opening Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={Object.entries(opening_performance).map(([opening, data]) => ({
              opening,
              games: data.games,
              accuracy: data.accuracy
            }))}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="opening" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip
                contentStyle={{ background: '#1e1e1e', border: '1px solid #667eea' }}
                labelStyle={{ color: '#fff' }}
              />
              <Legend wrapperStyle={{ color: '#fff' }} />
              <Bar dataKey="accuracy" fill="#667eea" />
              <Bar dataKey="games" fill="#4CAF50" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
