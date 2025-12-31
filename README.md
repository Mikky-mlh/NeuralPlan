# 🧠 NeuralPlan

**Turn dead time into growth.** An AI-powered productivity engine that converts cancelled classes into personalized study sessions.

## 🎯 The Problem

Students waste hours when classes get cancelled. Without a plan, that "free time" becomes Instagram scrolling time.

## 💡 Our Solution

NeuralPlan uses Google Gemini AI to generate study plans that:
- **Match your mood** (Zombie 🧟 → Beast Mode 🦁)
- **Time-boxed** (15-min chunks, not vague "study harder" advice)
- **Track accountability** (log what you ACTUALLY did)

## ✨ Key Features

### 1. Vision AI Timetable Parser
Upload your timetable image → AI extracts your schedule automatically

### 2. Mood-Adaptive Plans
- **Zombie Mode**: Passive learning (videos, summaries)
- **Beast Mode**: Active practice (problems, coding)

### 3. Accountability Tracking
- Log actual study time vs planned time
- See efficiency scores over time
- Historical data with charts

### 4. Professional UI
- Glassmorphism design
- Smooth animations
- Dark mode optimized

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **AI**: Google Gemini API (study plan generation + image parsing)
- **Data Viz**: Plotly (charts and graphs)
- **Storage**: CSV (demo), easily upgradable to PostgreSQL

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/NeuralPlan.git
cd NeuralPlan

# Install dependencies
pip install -r requirements.txt

# Add API key (create .streamlit/secrets.toml)
echo 'GEMINI_API_KEY_1 = "your_key_here"' > .streamlit/secrets.toml

# Run app
streamlit run app.py
```

Visit http://localhost:8501

## 📊 How It Works

1. **Schedule** → Upload your timetable (or edit manually)
2. **Mark Cancelled** → Change status when class is cancelled
3. **Get AI Plan** → Choose subject, time, and mood → Get personalized study plan
4. **Track Progress** → Log what you actually studied → See efficiency scores

## 🏆 Hackathon Info

**Build Time**: 7 days  
**Team**: Yuvraj Sarathe  
**License**: MIT

## 📝 Known Limitations

- **Single-user optimized**: CSV storage works for demos. Multi-user would need a database.
- **API rate limits**: Uses multiple API keys with automatic fallback.

## 🔮 Future Plans

- [ ] Real-time notifications (Twilio SMS when class cancelled)
- [ ] PostgreSQL for multi-user support
- [ ] Mobile app (React Native)
- [ ] Study streak gamification
- [ ] Integration with Google Calendar

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**Made with ❤️ and ☕ in 7 days**
