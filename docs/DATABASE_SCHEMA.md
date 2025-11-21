# Database Schema

SQLite database schema for AI Chess Trainer.

## Overview

**Database**: `data/chess_trainer.db` (SQLite 3)
**ORM**: SQLAlchemy
**Tables**: 4

---

## Tables

### 1. games

Stores analyzed chess games.

```sql
CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pgn TEXT NOT NULL,
    white_player VARCHAR(255),
    black_player VARCHAR(255),
    result VARCHAR(10),
    date DATE,
    event VARCHAR(255),
    site VARCHAR(255),
    eco_code VARCHAR(10),
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analyzed_at TIMESTAMP
);
```

**Columns**:
- `id`: Unique game identifier
- `pgn`: Complete game in PGN format
- `white_player`: White player name
- `black_player`: Black player name
- `result`: Game result (1-0, 0-1, 1/2-1/2, *)
- `date`: Game date
- `event`: Tournament/event name
- `site`: Location
- `eco_code`: Opening ECO code
- `imported_at`: When game was imported
- `analyzed_at`: When game was analyzed

**Indexes**:
- `idx_games_players` on (`white_player`, `black_player`)
- `idx_games_date` on (`date`)

---

### 2. game_analysis

Stores analysis results for games.

```sql
CREATE TABLE game_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    move_number INTEGER NOT NULL,
    move_san VARCHAR(20) NOT NULL,
    move_uci VARCHAR(10) NOT NULL,
    fen_before TEXT NOT NULL,
    fen_after TEXT NOT NULL,
    score_before INTEGER,
    score_after INTEGER,
    best_move VARCHAR(10),
    evaluation_loss INTEGER,
    classification VARCHAR(20),
    comment TEXT,
    analysis_depth INTEGER,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
);
```

**Columns**:
- `id`: Unique analysis entry identifier
- `game_id`: Reference to games table
- `move_number`: Move number in game
- `move_san`: Move in SAN notation (e.g., "Nf3")
- `move_uci`: Move in UCI notation (e.g., "g1f3")
- `fen_before`: FEN position before move
- `fen_after`: FEN position after move
- `score_before`: Evaluation before move (centipawns)
- `score_after`: Evaluation after move (centipawns)
- `best_move`: Engine's best move
- `evaluation_loss`: Centipawn loss
- `classification`: blunder|mistake|inaccuracy|good|excellent
- `comment`: AI-generated feedback (optional)
- `analysis_depth`: Stockfish depth used
- `analyzed_at`: Analysis timestamp

**Indexes**:
- `idx_analysis_game` on (`game_id`)
- `idx_analysis_classification` on (`classification`)

**Classification Thresholds**:
- **blunder**: loss >= 300cp
- **mistake**: 100cp <= loss < 300cp
- **inaccuracy**: 50cp <= loss < 100cp
- **good**: 0cp <= loss < 50cp
- **excellent**: loss < 0cp (improvement)

---

### 3. training_sessions

Stores training session data.

```sql
CREATE TABLE training_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    difficulty VARCHAR(20),
    focus VARCHAR(50),
    positions_attempted INTEGER DEFAULT 0,
    positions_correct INTEGER DEFAULT 0,
    avg_time_per_position FLOAT,
    total_score INTEGER DEFAULT 0
);
```

**Columns**:
- `id`: Session identifier
- `user_id`: User identifier (future multi-user support)
- `started_at`: Session start time
- `ended_at`: Session end time
- `difficulty`: beginner|intermediate|advanced
- `focus`: tactics|endgame|opening|general
- `positions_attempted`: Number of positions tried
- `positions_correct`: Number of correct solutions
- `avg_time_per_position`: Average solve time (seconds)
- `total_score`: Cumulative score

**Indexes**:
- `idx_sessions_user` on (`user_id`)
- `idx_sessions_date` on (`started_at`)

---

### 4. user_progress

Tracks user improvement over time.

```sql
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE NOT NULL,
    games_analyzed INTEGER DEFAULT 0,
    avg_accuracy FLOAT,
    total_blunders INTEGER DEFAULT 0,
    total_mistakes INTEGER DEFAULT 0,
    total_inaccuracies INTEGER DEFAULT 0,
    total_moves INTEGER DEFAULT 0,
    training_sessions INTEGER DEFAULT 0,
    training_accuracy FLOAT,
    rating_estimate INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns**:
- `id`: Progress entry identifier
- `user_id`: User identifier
- `date`: Date of progress record
- `games_analyzed`: Games analyzed on this date
- `avg_accuracy`: Average move accuracy (%)
- `total_blunders`: Blunders made
- `total_mistakes`: Mistakes made
- `total_inaccuracies`: Inaccuracies made
- `total_moves`: Total moves analyzed
- `training_sessions`: Training sessions completed
- `training_accuracy`: Training accuracy (%)
- `rating_estimate`: Estimated rating based on play
- `updated_at`: Last update timestamp

**Indexes**:
- `idx_progress_user_date` on (`user_id`, `date`)

**Unique Constraint**: (`user_id`, `date`)

---

## Relationships

```
games (1) ──< (N) game_analysis
  └─ One game has many analysis entries

user (implied) ──< (N) training_sessions
  └─ One user has many training sessions

user (implied) ──< (N) user_progress
  └─ One user has many progress records
```

---

## Queries

### Common Queries

#### Get all games
```sql
SELECT * FROM games ORDER BY date DESC LIMIT 10;
```

#### Get game with analysis
```sql
SELECT 
    g.*,
    COUNT(ga.id) as total_moves,
    SUM(CASE WHEN ga.classification = 'blunder' THEN 1 ELSE 0 END) as blunders,
    SUM(CASE WHEN ga.classification = 'mistake' THEN 1 ELSE 0 END) as mistakes,
    AVG(ga.evaluation_loss) as avg_cp_loss
FROM games g
LEFT JOIN game_analysis ga ON g.id = ga.game_id
WHERE g.id = ?
GROUP BY g.id;
```

#### Get user statistics
```sql
SELECT 
    COUNT(DISTINCT date) as days_active,
    SUM(games_analyzed) as total_games,
    AVG(avg_accuracy) as overall_accuracy,
    SUM(total_blunders) as total_blunders,
    SUM(total_mistakes) as total_mistakes
FROM user_progress
WHERE user_id = ?;
```

#### Get accuracy trend
```sql
SELECT 
    date,
    avg_accuracy
FROM user_progress
WHERE user_id = ?
ORDER BY date DESC
LIMIT 30;
```

---

## Database Operations

### Initialization

```python
from src.data.database import Database

db = Database()
db.create_tables()  # Creates all tables
```

### Adding a Game

```python
db.save_game(pgn_string)
```

### Saving Analysis

```python
db.save_analysis(game_id, analysis_dict)
```

### Retrieving Statistics

```python
stats = db.get_user_statistics(user_id)
```

---

## Migrations

Currently using SQLAlchemy without Alembic.

**Future**: Add Alembic for schema migrations.

### Manual Migration Example

```sql
-- Add new column
ALTER TABLE games ADD COLUMN time_control VARCHAR(20);

-- Create index
CREATE INDEX idx_games_time_control ON games(time_control);
```

---

## Backup & Restore

### Backup

```bash
# SQLite backup
sqlite3 data/chess_trainer.db ".backup data/backup.db"

# Or copy file
cp data/chess_trainer.db data/backup_$(date +%Y%m%d).db
```

### Restore

```bash
cp data/backup.db data/chess_trainer.db
```

---

## Performance Considerations

1. **Indexes**: Key columns indexed for fast queries
2. **Foreign Keys**: CASCADE delete for cleanup
3. **Transactions**: Use for bulk inserts
4. **Vacuum**: Run periodically to reclaim space

```bash
# Vacuum database
sqlite3 data/chess_trainer.db "VACUUM;"
```

---

## Future Enhancements

- [ ] Add user authentication table
- [ ] Add opening repertoire table
- [ ] Add puzzle table
- [ ] Add achievements table
- [ ] Add social features (friends, sharing)
- [ ] Add game collections/folders
- [ ] Add annotations/comments table
- [ ] Add full-text search on PGNs

---

See [src/data/database.py](../src/data/database.py) for implementation.
