# Silicon Valley Trail 🚀

A replayable, resource-management simulation game inspired by _The Oregon Trail_, where you guide a scrappy startup team from San Jose to San Francisco.

Each day (turn), your team travels, consumes resources, encounters events, and makes critical decisions that determine survival and success.

---

## 🎯 Overview

- Travel between real-world locations in Silicon Valley
- Manage limited resources while navigating unpredictable events
- Make strategic decisions with tradeoffs and consequences
- Reach your destination before your startup collapses

---

## 🧠 Core Concept

Each turn:

- Choose an action (minimum 3 options)
- Resolve outcomes based on current state + randomness + API data
- Update resources and game state
- Trigger an event at each location

Winning:

- Successfully reach the final destination

Losing:

- Run out of critical resources (cash, morale, coffee, etc.)

---

## ⚙️ Core Requirements

### 1. Game Loop

- Turn-based system (days)
- Each turn includes:
  - Player chooses an action:
    - Travel
    - Rest
    - Hackathon
    - Pitch VCs
    - Detour for supplies
  - Outcomes are resolved
  - Event is triggered

---

### 2. Resources & Stats

Track at least 3 meaningful resources:

Examples:

- 💰 Cash
- ☕ Coffee
- 😊 Team Morale
- 🐛 Bug Count
- 📈 Hype
- 🧠 Compute Credits
- 🧱 Tech Debt

Rules:

- Reaching destination = win
- Lose if:
  - Cash = 0
  - Morale collapses
  - No coffee for 2 turns

---

### 3. Map

- Minimum 10 real-world locations
- Example route:
  - San Jose → Palo Alto → Mountain View → Redwood City → San Mateo → San Francisco

- Visual map not required

---

### 4. Events & Choices

- Events occur after each movement
- Events are:
  - Semi-random or randomized
  - Influenced by game state and/or API data

Examples:

- Server outage → increase bugs
- VC pitch → gain cash or lose morale
- Hackathon → reduce bugs but consume coffee

Choices must involve tradeoffs:

- Risk vs reward
- Resource exchange

---

### 5. Public API Integration (Required)

At least one public API must influence gameplay (not just display).

#### Example APIs

**1. Weather (Open-Meteo / OpenWeather)**

- Rain → slower travel
- Heat → morale drops
- Cold → more coffee consumption

**2. Mapping (OpenStreetMap / Mapbox)**

- Distance affects travel cost
- Longer routes → higher resource usage

**3. Flight Tracking (OpenSky)**

- Nearby aircraft → supply drop
- Boost coffee or cash

**4. News/Trends (Hacker News API)**

- Trending topics → increase hype
- High hype + low morale → burnout risk

---

### 🧪 API Requirements

- Use real or cached responses
- Must affect gameplay logic
- Provide fallback (mock data) when:
  - No API key
  - Offline mode
  - API failure

---

## ✅ Required Features

### Testing

- Unit tests for:
  - Game loop logic
  - Resource updates
  - Win/Lose conditions

---

### Documentation

- README (this file)
- Design Notes (see below)

---

### Safety & Best Practices

- No hardcoded API keys
- Use environment variables (`.env`)
- Handle:
  - API errors
  - Timeouts
  - Rate limits
- No personal user data collected

---

## 🚀 Installation

```bash
python -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
python -m pip install flask

```

### Run:

- flask run 
- python app.py
- python -m flask --app game run --port 8000 --debug
- flask --app game run --port 8000 --debug

```bash
bash start.sh
chmod +x start.sh
./start.sh 
```

#### Generate requirements file:
each library installation - dont forget to add into requirement txt 
```bash
$ pip freeze > requirements.txt
```

## Database 

### Creating database 

## db migration (apply database schema changes safely)
flask db init 
flask db migrate -m "Initial migration." # initial migration 
flask db upgrade # apply changes 

export FLASK_APP=game
export FLASK_APP=1
flask shell 
flask run # run dev server 

## To check tables etc in sqlite database 
sqlite3 instance/dev.db ".tables"
sqlite3 instance/dev.db "SELECT COUNT(*) FROM game_session;"
sqlite3 instance/dev.db "SELECT COUNT(*) FROM location;"
sqlite3 instance/dev.db "SELECT id, current_day, status, cash, morale FROM game_session;"
sqlite3 instance/dev.db "SELECT * FROM game_session;"
sqlite3 instance/dev.db "SELECT *  FROM locations;"

### testing 

This project includes unit tests for critical game logic using pytest, including:

- resource updates
- win/lose conditions
- turn progression
- travel behavior
- event choice handling

Run tests with:

$ coverage run -m pytest
$ pytest -v # more details
$ pytest tests/test_name.py -v # run single file
pytest tests/test-actions.py - pass 
pytest tests/test-events.py - pass
pytest tests/test-status.py - pass 
pytest tests/test-weather.py - pass 

