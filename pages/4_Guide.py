import streamlit as st
from src.logo_helper import get_logo_html

with st.sidebar:
    st.markdown(get_logo_html(), unsafe_allow_html=True)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 3rem; color: #FF8C42;">📚 How to Use Neural Plan</h1>
    <p style="font-size: 1.2rem; color: #9aa0a6;">Complete walkthrough for maximizing your productivity</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## 🎯 Quick Start (3 Minutes)

### Step 1: Setup Your Schedule
1. Go to the **Schedule** page (left sidebar)
2. You'll see sample data - this is just for demo
3. **Option A**: Upload your actual timetable image/PDF
   - Click "Upload New Timetable" expander
   - Drop your timetable file
   - AI will extract your schedule automatically
4. **Option B**: Edit the table manually
   - Click any cell to edit
   - Change times, subjects, durations
   - Click "Save Daily Status" when done

---

### Step 2: Mark Cancelled Classes
When a class gets cancelled:
1. Go to **Schedule** page
2. Find that class in the table
3. Click the "Status" cell
4. Change from "Active" to "Cancelled"
5. Click "Save Daily Status"

---

### Step 3: Get Your AI Study Plan
1. Go to **Neural Coach** page (sidebar)
2. You'll see cancelled classes listed
3. Fill out the form:
   - **Subject**: Pick what to study (or let AI decide)
   - **Focus Topic**: Be specific (e.g., "recursion" not just "DSA")
   - **Confidence**: Rate 1-10 how well you know this
   - **Time Available**: Slider (15-180 minutes)
   - **Energy Level**: THIS IS CRUCIAL 👇
     
     - **Low Battery 😴**: Exhausted - AI gives passive tasks (watch videos, read summaries)
     - **Power Saving 😐**: Tired but functional - easy review tasks
     - **Normal Mode 🙂**: Standard difficulty - balanced mix
     - **Neural Sync 🧘**: Focused - harder challenges
     - **Beast Mode 🦁**: Peak performance - toughest material

4. Click "Generate Adaptive Plan"
5. AI creates a minute-by-minute study plan matching YOUR energy

---

### Step 4: Track What You Actually Did
After studying:
1. Go to **Insights** page
2. You'll see your cancelled classes
3. **BE HONEST**: Log actual study minutes in "Actual Work (Min)" column
4. If you studied something different, enter it in "What Did You Study?"
5. Click "Save Progress"
6. See your **Efficiency Score**: (Actual Work / Goal Time) × 100

---

## 🧠 Understanding the Energy System

### Why Energy Level Matters
Your brain's capacity changes throughout the day:
- **Morning after sleep**: Usually high energy (Beast Mode)
- **After lunch**: Energy dip (Power Saving)
- **Late night**: Either wired (Neural Sync) or dead (Low Battery)

Traditional study plans ignore this. Neural Plan adapts.

### What Each Mode Actually Means

**Low Battery 😴** (You can barely think):
- AI suggests: YouTube videos, podcasts, reading summaries
- NO practice problems, NO coding, NO writing
- Goal: Absorb information passively

**Power Saving 😐** (Functional but tired):
- AI suggests: Review notes, flashcards, easy examples
- Light problem-solving only
- Goal: Reinforce what you know

**Normal Mode 🙂** (Default state):
- AI suggests: Balanced mix - study + practice
- Standard difficulty problems
- Goal: Make steady progress

**Neural Sync 🧘** (Focused and calm):
- AI suggests: Deep work - hard problems, projects
- Conceptual understanding work
- Goal: Tackle challenging material

**Beast Mode 🦁** (Peak performance):
- AI suggests: Most difficult material, speed practice
- Competitive problem-solving
- Goal: Maximum output

---

## 📊 Reading Your Insights Page

### The Efficiency Score Explained
- **0-25%**: Wasted most of your time
- **25-50%**: Some effort but lots of procrastination
- **50-75%**: Decent work, room to improve
- **75-90%**: Strong performance, nearly optimal
- **90-100%**: Perfect or nearly perfect execution
- **100%+**: You studied MORE than planned (overachiever)

### The Charts Tell Stories
**"Goal vs. Execution" Bar Chart**:
- Blue bars = What you planned
- Red bars = What you actually did
- Gap between them = Your accountability gap

**"Efficiency Trend" Line Chart**:
- Shows last 7 days
- Look for patterns: Do you slack on weekends? Mondays?
- Red dashed line = 50% threshold (minimum acceptable)

---

## 🔥 Advanced Tips

### The Midnight Reset Behavior
**IMPORTANT**: Every day at 12:00 AM midnight:
- All cancelled classes → back to "Active"
- Daily state resets
- History is saved first

**Why this matters**: If you cancel Monday's 9 AM class, it stays cancelled ALL DAY Monday. But at midnight, it resets for Tuesday's schedule.

### Multiple Cancelled Classes Strategy
Let's say 3 classes cancelled = 180 minutes free:
- DON'T try to study 3 subjects (context switching kills focus)
- Pick ONE subject you're behind in
- Use the full 180 minutes on that

### The "AI Decide" Option
When you're overwhelmed and can't choose:
- Select "🤖 Let AI Decide" in Neural Coach
- AI analyzes your schedule and suggests best use of time

---

## 🐛 Troubleshooting

### "AI isn't generating plans!"
**Solutions**:
- Wait 5 minutes and try again (rate limit)
- Check your internet
- Try a shorter time window (60 min instead of 180 min)

### "My uploaded timetable wasn't recognized"
**Solutions**:
- Use a clear, high-resolution photo
- Make sure lighting is good (no shadows)
- Try PDF instead of image
- If all else fails: Edit manually

### "Efficiency score shows 0% but I studied!"
**Solutions**:
- Insights page ONLY tracks cancelled classes
- Make sure class was marked "Cancelled" in Schedule page
- Click "Save Progress" in Insights after logging

---

## 💡 Philosophy: Why This App Exists

Traditional productivity apps give you a blank todo list and say "good luck."

Neural Plan recognizes:
1. **Time is unpredictable** - Classes get cancelled, plans change
2. **Energy varies** - You're not a robot running at 100% all day
3. **Accountability matters** - Logging actual work builds discipline
4. **AI should adapt to YOU** - Not force you into rigid systems

The goal isn't perfection. It's **turning dead time into something useful** while respecting your human limitations.

---

## 🚀 Best Practices

### Daily Habits
1. **Morning**: Review schedule, mentally prepare for potential cancellations
2. **When class cancelled**: IMMEDIATELY go to Neural Coach (don't open Instagram first)
3. **After studying**: Log actual time within 1 hour (while memory is fresh)
4. **Evening**: Check Insights to see daily efficiency

### Weekly Review
- Look at 7-day efficiency trend
- Identify patterns: Which days do you slack? Which days are productive?
- Adjust: If Mondays suck, maybe plan easier tasks on Mondays

---

## ❓ FAQ

**Q: Does the app work offline?**
A: No. AI features need internet. But schedule editing works offline.

**Q: Can I use this for non-study activities?**
A: Yes! Mark "Gym" or "Guitar Practice" as subjects. AI adapts.

**Q: Is my data private?**
A: Yes. Everything is stored locally in CSV files on your computer.

**Q: Why CSV files instead of a real database?**
A: Speed. This is a hackathon project. CSV works perfectly for demos and personal use.

---

## 🎓 Example Workflow (Real Life)

**Scenario**: It's Tuesday 10 AM. Your 11 AM Calculus class just got cancelled (60 minutes free).

**Without Neural Plan**:
- Open phone → Scroll Instagram for 45 minutes → Feel guilty → Cram 15 minutes of panic studying
- Result: Wasted time + guilt

**With Neural Plan**:
1. Open app → Schedule page
2. Mark Calculus as "Cancelled"
3. Go to Neural Coach
4. Select: Subject: Calculus, Focus: "Derivatives chain rule", Confidence: 4/10, Time: 60 minutes, Energy: Normal Mode 🙂
5. Click Generate
6. AI creates plan with minute-by-minute breakdown
7. Follow plan
8. After 60 minutes: Log 55 minutes actual work
9. Efficiency: 92%
10. Feel accomplished instead of guilty

**Result**: Recovered 55 productive minutes from chaos.

---

**Remember**: The app is a tool, not a tyrant. If your efficiency is 40% but you learned something, that's still better than 0%.
""")
