# ChmodHero 🦸‍♂️

**Learn Linux file permissions through real DevOps scenarios!**

ChmodHero is an interactive web-based game that teaches Linux file permissions (`chmod` commands) through hands-on practice with realistic DevOps situations. Instead of boring theory, you'll solve actual problems like fixing deployment scripts, securing SSH keys, and resolving production incidents.

[![🎮 PLAY ONLINE](https://img.shields.io/badge/🎮-PLAY_ONLINE-4CAF50?style=for-the-badge)](https://sohaib1khan.github.io/chmod-hero/)
[![📚 DOCUMENTATION](https://img.shields.io/badge/📚-DOCUMENTATION-2196F3?style=for-the-badge)](https://github.com/sohaib1khan/chmod-hero)

##  Features

- **Real-world scenarios**: SSH security, Docker builds, database backups, Kubernetes secrets
- **Progressive difficulty**: Start with basic `chmod +x` and work up to complex permission scenarios
- **Instant feedback**: Get immediate validation and helpful hints for your commands
- **Scoring system**: Earn points based on speed and accuracy
- **Leaderboard**: Compete with other DevOps learners
- **Cross-platform**: Runs on Windows, Linux, and macOS

## Quick Start

### Option: Run Locally

**Prerequisites:**
- Python 3.7 or higher
- pip (Python package installer)
- A modern web browser

**Installation:**

```bash
# 1. Clone the repository
git clone https://github.com/sohaib1khan/chmod-hero.git
cd chmod-hero

# 2. Create and activate virtual environment
python3 -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the game
python app.py

# 5. Open your browser and go to http://localhost:5000
```

## 🎮 How to Play

1. **Read the scenario**: Each level presents a real DevOps problem
2. **Analyze the file permissions**: Check what's wrong with the current permissions
3. **Enter your chmod command**: Type the command to fix the issue
4. **Get feedback**: Receive instant validation and explanations
5. **Level up**: Progress through increasingly challenging scenarios

### Example Scenarios

**Level 1: Deployment Script**
```
Problem: deploy.sh script exists but isn't executable
Current: -rw-r--r-- deploy.sh
Solution: chmod +x deploy.sh
```

**Level 2: SSH Key Security**
```
Problem: SSH private key has wrong permissions (security risk!)
Current: -rw-r--r-- id_rsa
Solution: chmod 600 id_rsa
```

## What You'll Learn

- **Basic chmod syntax**: Understanding octal notation (755, 644, 600)
- **Symbolic notation**: Using +x, u+rwx, go-w syntax
- **Security best practices**: Proper permissions for different file types
- **Real-world applications**: SSH keys, scripts, config files, secrets
- **DevOps scenarios**: Docker builds, Kubernetes deployments, database operations

## Project Structure

```
chmod-hero/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── config.py             # Game configuration
├── README.md             # This file
├── docs/                 # GitHub Pages site
│   ├── index.html
│   └── style.css
├── static/               # CSS, JS, images
│   ├── css/style.css
│   └── js/game.js
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── game.html
│   ├── help.html
│   ├── tutorial.html
│   └── leaderboard.html
├── game/                 # Game logic
│   ├── __init__.py
│   ├── scenarios.py      # Game scenarios and levels
│   ├── permissions.py    # Permission validation
│   └── scoring.py        # Score calculation
└── tests/               # Unit tests
    ├── __init__.py
    └── test_permissions.py
```

## Development

### Adding New Scenarios

Edit `game/scenarios.py` to add new levels:

```python
{
    'title': 'Your Scenario Title',
    'description': 'Describe the problem situation',
    'context': 'DevOps Context (e.g., CI/CD Pipeline)',
    'files': [
        {'name': 'filename.ext', 'current_permissions': 'rw-r--r--', 'octal': '644'}
    ],
    'task': 'What the player needs to accomplish',
    'expected_command': 'chmod 755 filename.ext',
    'alternative_commands': ['chmod +x filename.ext'],
    'explanation': 'Why this solution works',
    'difficulty': 'easy|medium|hard',
    'points': 200
}
```

### Running Tests

```bash
python -m pytest tests/
```

### Environment Variables

For production deployment, set these environment variables:

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export DEBUG=false
```

## Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Game Levels

| Level | Scenario | Difficulty | Concepts |
|-------|----------|------------|----------|
| 1 | Deployment Script | Easy | Basic +x permissions |
| 2 | SSH Key Security | Easy | 600 permissions, security |
| 3 | Configuration Files | Medium | 644 permissions, multiple files |
| 4 | Container Build | Medium | 754 permissions, build scripts |
| 5 | Database Backup | Hard | 750 permissions, group access |
| 6 | Kubernetes Secrets | Hard | 600 permissions, security audit |
| 7 | Git Hooks | Medium | 755 permissions, development tools |

## Troubleshooting

**Game won't start**
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Check Python version: `python --version` (needs 3.7+)
- Reinstall dependencies: `pip install -r requirements.txt`

**Commands not working**
- Check your syntax carefully (chmod is case-sensitive)
- Try alternative formats (755 vs +x)
- Use the hint button for guidance

**Leaderboard not saving**
- Check file permissions in the project directory
- Make sure scores.json can be created/modified
