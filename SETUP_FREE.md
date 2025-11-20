# Free Setup Guide for Kids

Get started with AI Chess Trainer **completely free**! No API keys needed.

## Quick Setup (15 minutes)

### Step 1: Install Ollama (Free AI)

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from https://ollama.com/download

### Step 2: Download AI Model (One-Time, ~3GB)

```bash
# For beginners/kids (smaller, faster)
ollama pull llama3.2:3b

# For better quality (if you have more RAM)
ollama pull llama3.1:8b
```

### Step 3: Download Stockfish Chess Engine

**Linux:**
```bash
sudo apt-get install stockfish
```

**Mac:**
```bash
brew install stockfish
```

**Windows:**
1. Download from https://stockfishchess.org/download/
2. Extract to `C:\Program Files\Stockfish\`
3. Add to PATH or note the location

### Step 4: Install Python Dependencies

```bash
cd AI-Chess-Trainer
pip install -r requirements.txt
```

### Step 5: Configure (No API Keys!)

```bash
cp .env.example .env
```

Edit `.env` and set:
```env
# AI Provider (use free Ollama)
AI_PROVIDER=ollama
AI_MODEL=llama3.2:3b

# Chess Engine Path
STOCKFISH_PATH=/usr/local/bin/stockfish
# Or Windows: C:\Program Files\Stockfish\stockfish.exe
```

### Step 6: Test It!

```bash
# Test Ollama
python -m src.ai.ollama_client

# Test full system
python -m src.ui.cli --help
```

## Usage Examples

### Analyze a Game (Free!)
```bash
chess-trainer analyze my_game.pgn --save
```

### Interactive Training
```bash
chess-trainer train --type tactical --count 5
```

### View Progress
```bash
chess-trainer stats
```

## For Teachers & Chess Clubs

### Setup on School Computer
1. Install Ollama (admin rights needed)
2. Download model once (all students share it)
3. Each student uses own account for progress tracking
4. **Total cost: $0** forever!

### Performance Tips
- **3B model**: Works on any modern laptop (8GB RAM)
- **8B model**: Better quality, needs 16GB RAM
- **GPU**: Not required but speeds up by 2-3x

### Offline Use
After initial setup, works **completely offline**:
- ✅ Game analysis
- ✅ AI explanations
- ✅ Training puzzles
- ✅ Progress tracking

No internet needed after downloading the model!

## Troubleshooting

### "Ollama not running"
```bash
# Start Ollama service
ollama serve
```

### "Model not found"
```bash
# Download the model
ollama pull llama3.2:3b
```

### "Stockfish not found"
```bash
# Find stockfish location
which stockfish  # Linux/Mac
where stockfish  # Windows

# Update .env with correct path
```

### Slow responses
```bash
# Use smaller model
ollama pull llama3.2:3b

# Or use rule-based explanations (instant)
# Edit config to use hybrid mode
```

## What You Get (All Free!)

✅ **Unlimited game analysis** - analyze as many games as you want
✅ **AI explanations** - understand why moves are good/bad
✅ **Interactive training** - practice specific positions
✅ **Progress tracking** - see your improvement over time
✅ **Tactical puzzles** - millions from Lichess database
✅ **Privacy** - all data stays on your computer

## Cost Comparison

| Feature | Paid (Claude) | Free (Ollama) |
|---------|--------------|---------------|
| Setup | $0 | $0 |
| Per game | $0.01-0.05 | $0 |
| Monthly (100 games) | $1-5 | $0 |
| Annual (school) | $500-1000 | $0 |
| **Electricity** | - | ~$0.10/day |

## Laptop Requirements

### Minimum (3B model)
- CPU: Dual-core (i3/Ryzen 3)
- RAM: 8GB
- Storage: 20GB free
- Response time: 2-5 seconds

### Recommended (8B model)
- CPU: Quad-core (i5/Ryzen 5)
- RAM: 16GB
- Storage: 30GB free
- Response time: 1-3 seconds

### With GPU (Optional)
- Any NVIDIA GPU with 4GB+ VRAM
- 2-3x faster responses

## Advanced: Training Custom Model

Want a model **specialized for chess**?

### Option 1: Fine-tune Llama 3.2
1. Generate training data (1000+ positions with explanations)
2. Use your current Stockfish analyses
3. Fine-tune with LoRA (~4 hours on GPU)
4. Result: Chess-specialized model

### Option 2: Use Existing Models
Check Hugging Face for chess-specific models:
```bash
# Search for chess models
ollama pull chess-instructor:7b  # If available
```

## Next Steps

1. ✅ Complete setup above
2. ✅ Try analyzing a sample game
3. ✅ Add your own games
4. ✅ Start training!

## Support

Having issues? Check:
1. [NO_COST_APPROACH.md](docs/NO_COST_APPROACH.md) - detailed architecture
2. [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) - roadmap
3. Ollama docs: https://ollama.com/
4. Stockfish docs: https://stockfishchess.org/

---

**Remember**: This is 100% free and perfect for:
- 👶 Kids learning chess
- 🏫 Schools and chess clubs
- 🏠 Homeschooling
- 🎓 Educational programs
- 💰 Anyone on a budget

No hidden costs, no subscriptions, no API limits!
