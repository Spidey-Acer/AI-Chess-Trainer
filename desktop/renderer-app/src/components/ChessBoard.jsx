import React from 'react';
import { Chessboard } from 'react-chessboard';

export default function ChessBoardComponent({
  position,
  onPieceDrop,
  boardWidth = 400,
  customSquareStyles = {}
}) {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '20px'
    }}>
      <Chessboard
        position={position}
        onPieceDrop={onPieceDrop}
        boardWidth={boardWidth}
        customSquareStyles={customSquareStyles}
      />
    </div>
  );
}
