# ChmodHero 🦸‍♂️

<div align="center">

**Learn Linux file permissions through real DevOps scenarios!**

ChmodHero is an interactive web-based game that teaches Linux file permissions (`chmod` commands) through hands-on practice with realistic DevOps situations. Instead of boring theory, you'll solve actual problems like fixing deployment scripts, securing SSH keys, and resolving production incidents.

[![🎮 INTERACTIVE](https://img.shields.io/badge/🎮-INTERACTIVE-ff6b6b?style=for-the-badge)](https://sohaib1khan.github.io/chmod-hero/)
[![📚 DOCUMENTATION](https://img.shields.io/badge/📚-DOCUMENTATION-4ecdc4?style=for-the-badge)](https://github.com/sohaib1khan/chmod-hero/blob/main/README.md)

🎯 **Real-world Learning** | 🚀 **Progressive Difficulty** | ⚡ **Instant Feedback** | 🏆 **Gamified Experience**

*🔥 Production ready • Educational excellence • Always evolving*

</div>

---

## 🌟 Why ChmodHero?

<div align="center">

### 🎮 [**Try the Interactive Demo**](https://sohaib1khan.github.io/chmod-hero/) 🎮

*No installation required - start learning immediately!*

</div>

| Feature | Description |
|---------|-------------|
| 🎯 **Real DevOps Scenarios** | SSH security, Docker builds, database backups, Kubernetes secrets |
| 🚀 **Progressive Learning** | Start with basic `chmod +x` and work up to complex permission scenarios |
| ⚡ **Instant Feedback** | Get immediate validation and helpful hints for your commands |
| 🏆 **Scoring System** | Earn points based on speed and accuracy |
| 🏅 **Leaderboard** | Compete with other DevOps learners |
| 🌐 **Cross-Platform** | Runs on Windows, Linux, and macOS |

## 🚀 Quick Start

### 🌐 Option 1: Try Online (Recommended)
**[🎮 Launch ChmodHero](https://sohaib1khan.github.io/chmod-hero/)** - No installation required!

### 💻 Option 2: Run Locally

#### Prerequisites
- Python 3.7+ 
- pip (Python package installer)
- Modern web browser

#### Installation

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

# 5. Open your browser
# Navigate to http://localhost:5000
```

## 🎮 How to Play

<div align="center">

**[🚀 Start Playing Now](https://sohaib1khan.github.io/chmod-hero/)**

</div>

1. **📖 Read the scenario**: Each level presents a real DevOps problem
2. **🔍 Analyze permissions**: Check what's wrong with the current permissions
3. **⌨️ Enter your command**: Type the chmod command to fix the issue
4. **💡 Get feedback**: Receive instant validation and explanations
5. **📈 Level up**: Progress through increasingly challenging scenarios

### 🎯 Example Scenarios

<details>
<summary><strong>🚀 Level 1: Deployment Script</strong></summary>

```bash
Problem: deploy.sh script exists but isn't executable
Current: -rw-r--r-- deploy.sh
Task: Make the script executable for everyone
Solution: chmod +x deploy.sh
```
</details>

<details>
<summary><strong>🔐 Level 2: SSH Key Security</strong></summary>

```bash
Problem: SSH private key has wrong permissions (security risk!)
Current: -rw-r--r-- id_rsa
Task: Secure the key so only owner can access
Solution: chmod 600 id_rsa
```
</details>

<details>
<summary><strong>🐳 Level 4: Container Build</strong></summary>

```bash
Problem: Docker build failing due to script permissions
Current: -rw-rw-rw- build.sh
Task: Make executable but secure (owner: rwx, group: rx, others: r)
Solution: chmod 754 build.sh
```
</details>

## 📚 What You'll Master

| Concept | Description | Real-world Use |
|---------|-------------|----------------|
| **🔢 Octal Notation** | Understanding 755, 644, 600 | Script permissions, file security |
| **🔧 Symbolic Commands** | Using +x, u+rwx, go-w syntax | Quick permission fixes |
| **🛡️ Security Practices** | Proper permissions for different file types | SSH keys, configs, secrets |
| **🚀 DevOps Applications** | Docker builds, K8s deployments, CI/CD | Production environments |

## 🏗️ Project Structure

```
chmod-hero/
├── 🎮 app.py                 # Main Flask application
├── 📋 requirements.txt       # Python dependencies  
├── ⚙️ config.py             # Game configuration
├── 📖 README.md             # This file
├── 🌐 docs/                 # GitHub Pages site
│   ├── index.html
│   └── style.css
├── 🎨 static/               # CSS, JS, images
│   ├── css/style.css
│   └── js/game.js
├── 📄 templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── game.html
│   ├── help.html
│   ├── tutorial.html
│   └── leaderboard.html
├── 🎯 game/                 # Game logic
│   ├── __init__.py
│   ├── scenarios.py         # 7+ real DevOps scenarios
│   ├── permissions.py       # Permission validation
│   └── scoring.py           # Score calculation
└── 🧪 tests/               # Unit tests
    ├── __init__.py
    └── test_permissions.py
```

## 🛠️ Development

### 🎯 Adding New Scenarios

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

### 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

### 🌐 Environment Variables

For production deployment:

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export DEBUG=false
```

## 🚀 Deployment Options

### 🌐 GitHub Pages (Live Demo)
Visit: **[sohaib1khan.github.io/chmod-hero](https://sohaib1khan.github.io/chmod-hero/)**

### 💻 Local Development
```bash
python app.py
```

### 🏭 Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 🐳 Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 📊 Game Levels & Scenarios

| Level | Scenario | Difficulty | Key Concepts | Real-world Context |
|-------|----------|------------|--------------|-------------------|
| 1 | 🚀 Deployment Script | Easy | `chmod +x`, basic executable | CI/CD Pipeline |
| 2 | 🔐 SSH Key Security | Easy | `chmod 600`, private files | Security Audit |
| 3 | 📄 Config Files | Medium | `chmod 644`, readable files | Production Incident |
| 4 | 🐳 Container Build | Medium | `chmod 754`, build scripts | Docker/CI-CD |
| 5 | 💾 Database Backup | Hard | `chmod 750`, group permissions | Database Operations |
| 6 | ☸️ Kubernetes Secrets | Hard | `chmod 600`, K8s security | Container Security |
| 7 | 🔧 Git Hooks | Medium | `chmod 755`, development tools | Version Control |

## 🎯 Learning Outcomes

After completing ChmodHero, you'll be able to:

- ✅ **Confidently use chmod** in real DevOps scenarios
- ✅ **Secure SSH keys and sensitive files** properly
- ✅ **Fix permission issues** in CI/CD pipelines
- ✅ **Understand octal and symbolic** notation
- ✅ **Apply security best practices** in production
- ✅ **Debug permission problems** quickly

## 🐛 Troubleshooting

<details>
<summary><strong>🚫 Game won't start</strong></summary>

- Ensure you're in the virtual environment: `source venv/bin/activate`
- Check Python version: `python --version` (needs 3.7+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Try the online version: [sohaib1khan.github.io/chmod-hero](https://sohaib1khan.github.io/chmod-hero/)
</details>

<details>
<summary><strong>❌ Commands not working</strong></summary>

- Check syntax carefully (chmod is case-sensitive)
- Try alternative formats (755 vs +x)
- Use the hint button for guidance
- Refer to the help section in the game
</details>

<details>
<summary><strong>💾 Leaderboard not saving</strong></summary>

- Check file permissions in project directory
- Ensure scores.json can be created/modified
- Run with proper user permissions
</details>

## 🤝 Contributing

We welcome contributions! Here's how you can help:

- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest new scenarios** for additional DevOps contexts
- 🔧 **Submit pull requests** for improvements
- 📚 **Improve documentation** and tutorials
- ⭐ **Star the repository** if you find it useful!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ for the DevOps community
- Inspired by real-world permission challenges
- Thanks to all contributors and players!

---

<div align="center">

### 🎮 Ready to Become a Chmod Hero?

**[🚀 Start Playing Now](https://sohaib1khan.github.io/chmod-hero/)** | **[⭐ Star on GitHub](https://github.com/sohaib1khan/chmod-hero)** | **[🐛 Report Issues](https://github.com/sohaib1khan/chmod-hero/issues)**

*Stop struggling with Linux permissions. Learn through practice with real scenarios that you'll actually encounter in your DevOps career!*

</div>