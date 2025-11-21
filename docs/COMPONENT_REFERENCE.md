# React Component Reference

Documentation for all React components in the desktop app.

## Component Hierarchy

```
App (Router)
├── Sidebar Navigation
├── AnalyzePage
│   ├── ChessBoardComponent
│   └── AnalysisPanel
├── TrainingMode
│   ├── ChessBoardComponent
│   └── Training Panel
├── GameList
└── StatsDisplay
```

---

## App Component

**File**: `src/App.js`

Main application component with routing and navigation.

### Features
- React Router integration
- Sidebar navigation (4 routes)
- Main content area
- Status indicator

### Routes
- `/` → Redirects to `/analyze`
- `/analyze` → AnalyzePage
- `/train` → TrainingMode
- `/games` → GameList
- `/stats` → StatsDisplay

### State
```javascript
const [selectedGame, setSelectedGame] = useState(null);
```

---

## ChessBoardComponent

**File**: `src/components/ChessBoard.jsx`

Interactive chess board using react-chessboard.

### Props
```typescript
{
  position: string;           // FEN string
  onPieceDrop?: (from, to) => boolean;
  boardWidth?: number;        // Default: 400
  customSquareStyles?: object;
}
```

### Example
```jsx
<ChessBoardComponent
  position={chess.fen()}
  onPieceDrop={handleMove}
  boardWidth={450}
  customSquareStyles={{
    e4: { backgroundColor: 'rgba(255, 255, 0, 0.4)' }
  }}
/>
```

---

## AnalysisPanel

**File**: `src/components/AnalysisPanel.jsx`

Displays analysis results with evaluation bar and move list.

### Props
```typescript
{
  analysis: {
    score: number;
    best_move: string;
    evaluation: string;
    move_analysis: Array<{
      move_number: number;
      move: string;
      score_after: number;
      classification: 'blunder'|'mistake'|'inaccuracy'|'good';
    }>;
  } | null;
  loading: boolean;
}
```

### Features
- Evaluation bar (visual centipawn display)
- Best move display
- Move-by-move list
- Classification badges
- Loading spinner
- Empty state

### Styling
- `.analysis-panel` - Main container
- `.eval-bar` - Evaluation visualization
- `.move-item` - Individual move
- `.blunder`, `.mistake`, etc. - Classification styles

---

## GameList

**File**: `src/components/GameList.jsx`

Displays list of analyzed games.

### Props
```typescript
{
  onSelectGame: (game: object) => void;
}
```

### Features
- Async game loading
- Player names and result
- Accuracy display
- Click to select
- Empty state
- Error handling
- Retry button

### State
```javascript
const [games, setGames] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);
```

---

## TrainingMode

**File**: `src/components/TrainingMode.jsx`

Interactive training with position practice.

### Features
- Difficulty selector (beginner/intermediate/advanced)
- Interactive board
- Instant feedback
- Next position button
- Objective display
- Hints
- Score loss calculation

### State
```javascript
const [chess] = useState(new Chess());
const [position, setPosition] = useState(chess.fen());
const [trainingData, setTrainingData] = useState(null);
const [feedback, setFeedback] = useState(null);
const [difficulty, setDifficulty] = useState('intermediate');
const [loading, setLoading] = useState(false);
```

### Workflow
1. Load training position from API
2. User makes move on board
3. API validates move
4. Display feedback (correct/incorrect)
5. Show next position button

---

## StatsDisplay

**File**: `src/components/StatsDisplay.jsx`

Statistics dashboard with charts.

### Features
- Summary cards (4 metrics)
- Line chart (accuracy trend)
- Bar chart (opening performance)
- Responsive design
- Real-time data

### Charts
Uses Recharts library:
- `LineChart` - Accuracy over time
- `BarChart` - Opening performance

### Data Structure
```typescript
{
  total_games: number;
  avg_accuracy: number;
  total_blunders: number;
  total_mistakes: number;
  improvement_trend: Array<{
    date: string;
    accuracy: number;
  }>;
  opening_performance: {
    [opening: string]: {
      games: number;
      accuracy: number;
    };
  };
}
```

---

## AnalyzePage

**File**: `src/pages/AnalyzePage.jsx`

Dual-mode analysis page (position or game).

### Features
- Mode switcher (position/game)
- Chess board (position mode)
- PGN textarea (game mode)
- File import button
- Analyze button
- Reset button
- Integrated AnalysisPanel

### State
```javascript
const [chess] = useState(new Chess());
const [position, setPosition] = useState(chess.fen());
const [analysis, setAnalysis] = useState(null);
const [loading, setLoading] = useState(false);
const [pgnText, setPgnText] = useState('');
const [mode, setMode] = useState('position'); // 'position' or 'game'
```

### Modes
- **Position Mode**: Analyze current board position
- **Game Mode**: Analyze full PGN game

---

## Styling Conventions

### Color Palette
- Primary: `#667eea` (purple)
- Secondary: `#764ba2` (dark purple)
- Success: `#4CAF50` (green)
- Warning: `#FFC107` (yellow/gold)
- Error: `#f44336` (red)
- Background: `#121212` (dark)
- Panel: `#1e1e1e` (dark gray)

### Typography
- Font: System font stack
- Headings: Bold, color `#667eea`
- Body: White on dark background

### Animations
- Transitions: `0.3s ease`
- Hover: `translateY(-2px)` + shadow
- Spinner: Rotating border animation

---

## API Integration

All components use `src/services/api.js`:

```javascript
import {
  analyzePosition,
  analyzeGame,
  getTrainingPosition,
  checkMove,
  listGames,
  getStats
} from '../services/api';
```

---

## Best Practices

1. **Use functional components** with hooks
2. **Handle loading states** with spinners
3. **Handle errors** with error messages
4. **Provide empty states** when no data
5. **Use semantic HTML** for accessibility
6. **Keep components small** and focused
7. **Extract reusable logic** to custom hooks
8. **Style with CSS modules** or styled-components

---

## Future Enhancements

- [ ] Add unit tests (Jest + React Testing Library)
- [ ] Add TypeScript for type safety
- [ ] Add Storybook for component documentation
- [ ] Add accessibility tests
- [ ] Add performance monitoring
- [ ] Add error boundaries
- [ ] Add lazy loading for routes
- [ ] Add service worker for offline support

---

See [desktop/README.md](../desktop/README.md) for desktop app setup.
