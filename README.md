<div align="center">

![Neural Plan Logo](assets/logo.png)

# 🧠 Neural Plan

**Transform Cancelled Classes into Productive Study Sessions**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39+-FF4B4B.svg)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)

*An AI-powered study planner that adapts to your energy levels and turns wasted time into learning opportunities*

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Usage](#-usage) • [License](#-license)

</div>

---

## 🎯 Overview

Students waste hours on cancelled classes scrolling social media. **Neural Plan** uses Google Gemini AI to generate energy-adaptive study plans that match your mental state (Low Battery 😴 → Beast Mode 🦁) and track accountability through data-driven insights.

---

## ✨ Features

- **🤖 AI Study Plans**: 5 energy modes with minute-by-minute breakdowns
- **📸 Vision Parser**: Upload timetable images for automatic extraction
- **📊 Accountability**: Track efficiency with goal vs. actual comparisons
- **🎨 Modern UI**: Glassmorphism design with particle.js animations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

```bash
# Clone the repository
git clone https://github.com/Mikky-mlh/NeuralPlan.git
cd NeuralPlan

# Install dependencies
pip install -r requirements.txt
```

<details>
<summary><b>🔐 API Key Configuration (Click to expand)</b></summary>

<br>

**Important**: Never commit your API keys to version control!

1. Create the secrets file:
```bash
mkdir .streamlit
```

2. Create `.streamlit/secrets.toml` and add your key:
```toml
GEMINI_API_KEY_1 = "your_actual_api_key_here"
```

3. The `.gitignore` already excludes this file from git

**Optional**: Add backup keys for rate limit failover:
```toml
GEMINI_API_KEY_1 = "primary_key"
GEMINI_API_KEY_2 = "backup_key"
GEMINI_API_KEY_3 = "tertiary_key"
```

</details>

```bash
# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### First-Time Setup
1. Upload timetable or edit manually in Schedule page
2. Mark classes as "Cancelled" when needed
3. Generate AI study plan in Neural Coach
4. Log actual time in Insights page

---

## 📁 Repository Structure

```
NeuralPlan/
├── app.py                      # Main entry point with session state management
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
│
├── .streamlit/
│   ├── config.toml            # Streamlit theme configuration
│   └── static/
│       └── logo.png           # App logo
│
├── assets/
│   ├── logo.png               # Main logo image
│   ├── animation.json         # Lottie animation data
│   ├── style.css              # Global styles with glassmorphism
│   ├── stylesh.css            # Schedule page specific styles
│   ├── neural_coach.css       # Neural Coach page styles
│   └── data_page.css          # Insights page styles
│
├── data/
│   ├── default_schedule.csv   # Sample timetable (14 classes)
│   └── history.csv            # Sample historical data
│
├── pages/
│   ├── 1_Schedule.py          # Schedule management & upload
│   ├── 2_Neural_Coach.py      # AI study plan generator
│   ├── 3_Insights.py          # Analytics & progress tracking
│   └── 4_Guide.py             # User documentation
│
└── src/
    ├── __init__.py
    ├── gemini_client.py       # Google Gemini API integration
    ├── logo_helper.py         # Logo rendering utilities
    └── utils.py               # Helper functions (time conversion, etc.)
```

---

## 🏗️ Architecture

### System Flow Diagram

```mermaid
graph TB
    Start([User Opens App]) --> LoadState[Load Session State]
    LoadState --> CheckReset{Midnight<br/>Reset?}
    CheckReset -->|Yes| ResetDaily[Clear Daily State<br/>Restore Active Status]
    CheckReset -->|No| LoadSchedule[Load Schedule Data]
    ResetDaily --> LoadSchedule
    
    LoadSchedule --> MainApp[Main App Interface]
    
    MainApp --> Schedule[📅 Schedule Page]
    MainApp --> Coach[🧠 Neural Coach]
    MainApp --> Insights[📊 Insights]
    MainApp --> Guide[📚 Guide]
    
    Schedule --> Upload{Upload<br/>Timetable?}
    Upload -->|Yes| Vision[Gemini Vision API]
    Vision --> ParseCSV[Parse to CSV]
    ParseCSV --> SaveSchedule[(Save to<br/>user_schedule.csv)]
    
    Upload -->|No| ManualEdit[Manual Edit Table]
    ManualEdit --> MarkCancel[Mark Classes as Cancelled]
    MarkCancel --> SaveDaily[(Save to<br/>daily_state.csv)]
    
    SaveDaily --> Coach
    
    Coach --> CheckCancel{Cancelled<br/>Classes?}
    CheckCancel -->|No| ShowInfo[Show Info Message]
    CheckCancel -->|Yes| ShowForm[Display AI Form]
    
    ShowForm --> UserInput[User Selects:<br/>- Subject<br/>- Time<br/>- Energy Level<br/>- Focus Topic<br/>- Confidence]
    UserInput --> CallGemini[Gemini API Call]
    
    CallGemini --> GeneratePlan[Generate Adaptive<br/>Study Plan]
    GeneratePlan --> DisplayPlan[Display Markdown Plan]
    
    DisplayPlan --> Insights
    
    Insights --> LogActual[User Logs<br/>Actual Study Time]
    LogActual --> CalcEfficiency[Calculate Efficiency<br/>= Actual/Goal × 100]
    CalcEfficiency --> SaveHistory[(Update<br/>history.csv)]
    
    SaveHistory --> ShowCharts[Display Charts:<br/>- Goal vs Actual<br/>- 7-Day Trend<br/>- Efficiency Score]
    
    ShowCharts --> End([Session Continues])
    
    style Start fill:#2E3192,color:#fff
    style End fill:#FF8C42,color:#fff
    style Vision fill:#4285F4,color:#fff
    style CallGemini fill:#4285F4,color:#fff
    style SaveSchedule fill:#10B981,color:#fff
    style SaveDaily fill:#10B981,color:#fff
    style SaveHistory fill:#10B981,color:#fff
```

### Data Flow Architecture

```mermaid
flowchart LR
    subgraph Frontend["🎨 Streamlit Frontend"]
        UI[User Interface]
        Session[Session State]
    end
    
    subgraph Backend["⚙️ Python Backend"]
        App[app.py]
        Pages[Pages Module]
        Src[Source Module]
    end
    
    subgraph AI["🤖 AI Services"]
        Gemini[Google Gemini API]
        Vision[Gemini Vision]
    end
    
    subgraph Storage["💾 Data Layer"]
        CSV1[(default_schedule.csv)]
        CSV2[(user_schedule.csv)]
        CSV3[(daily_state.csv)]
        CSV4[(history.csv)]
    end
    
    UI <--> Session
    Session <--> App
    App <--> Pages
    Pages <--> Src
    
    Src <--> Gemini
    Src <--> Vision
    
    Src <--> CSV1
    Src <--> CSV2
    Src <--> CSV3
    Src <--> CSV4
    
    style Frontend fill:#2E3192,color:#fff
    style Backend fill:#1a1f2e,color:#fff
    style AI fill:#4285F4,color:#fff
    style Storage fill:#10B981,color:#fff
```

```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit 1.39+ | Rapid web app development |
| **AI Engine** | Google Gemini Flash | Study plan generation & OCR |
| **Data Viz** | Plotly 5.24+ | Interactive charts & graphs |
| **Animations** | Lottie, Particles.js | UI enhancements |
| **Storage** | CSV files | Lightweight data persistence |
| **Language** | Python 3.8+ | Core application logic |

---

## 📖 Usage

**Schedule**: Upload timetable image or manually edit → Mark cancelled classes → Save

**Neural Coach**: Select subject, time, energy level, focus topic → Generate AI plan

**Insights**: Log actual study minutes → View efficiency score `(Actual/Goal × 100)` → Analyze trends

---

## 🔧 Configuration

<details>
<summary><b>Theme Customization</b></summary>

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF8C42"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1a1f2e"
textColor = "#e8eaed"
```

</details>

<details>
<summary><b>Data Files Format</b></summary>

**Schedule** (`user_schedule.csv`):
```csv
Day,Time,Subject,Duration,Status,Actual_Study,Custom_Subject
Monday,09:00 AM,Data Structures,60,Active,0,
```

**History** (`history.csv`):
```csv
Date,Time_Saved,Time_Used,Efficiency,Classes_Cancelled
2025-01-01,120,90,75,2
```

</details>

---

## 🐛 Troubleshooting

- **AI not generating**: Check API key, wait 5 min (rate limit), verify internet
- **Upload failed**: Use high-res images, try PDF, or edit manually
- **0% efficiency**: Mark class as "Cancelled" in Schedule, click "Save Progress"

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team Nerd Herd

<div align="center">

![Nerd Herd Logo](assets/nerdherd.png)

**Built in 7 days for a hackathon challenge by:**

</div>

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/SourabhX16">
        <img src="https://github.com/SourabhX16.png" width="100px;" alt="Sourabh"/><br />
        <sub><b>Sourabh Patne</b></sub>
      </a><br />
      <a href="https://github.com/SourabhX16">GitHub</a> • <a href="http://linkedin.com/in/sourabh-patne-2385733a3">LinkedIn</a>
    </td>
    <td align="center">
      <a href="https://github.com/siddhikadhanelia">
        <img src="https://github.com/siddhikadhanelia.png" width="100px;" alt="Sidhika"/><br />
        <sub><b>Siddhika Dhanelia</b></sub>
      </a><br />
      <a href="https://github.com/siddhikadhanelia">GitHub</a> • <a href="https://www.linkedin.com/in/siddhika-dhanelia-20a67334a/">LinkedIn</a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/majorsandeep11">
        <img src="https://github.com/majorsandeep11.png" width="100px;" alt="Shlok"/><br />
        <sub><b>Shlok Pandey</b></sub>
      </a><br />
      <a href="https://github.com/majorsandeep11">GitHub</a> • <a href="https://in.linkedin.com/in/shlok-pandey-4902a83a2">LinkedIn</a>
    </td>
    <td align="center">
      <a href="https://github.com/Mikky-mlh">
        <img src="https://github.com/Mikky-mlh.png" width="100px;" alt="Yuvraj"/><br />
        <sub><b>Yuvraj Sarathe</b></sub>
      </a><br />
      <a href="https://github.com/Mikky-mlh">GitHub</a> • <a href="https://www.linkedin.com/in/yuvraj-sarathe">LinkedIn</a>
    </td>
  </tr>
</table>

---

<div align="center">

**⭐ Star this repo if Neural Plan helped you reclaim wasted time!**

Made with ❤️ and ☕ by **Team Nerd Herd**

</div>

