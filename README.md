# SILICON VALLEY TRAIL

## Project Overview

Silicon Valley Trail is a replayable, resource-management simulation game where you guide a scrappy startup team from San Jose to San Francisco. Each day (turn), your team travels, consumes resources, encounters events, and makes critical decisions that determine survival and success.

---

### Core Features 

### Tech Stack 
- **Frontend**: 
  - Jinja2
- **Backend**: 
  - Flask 
  - Database: SQLite + SQLAlchemy ORM
- **External APIs**:
  - OpenWeather
- **Testing**: 
  - Pytest

## Documentation

- [Quick Start](#quick-start)
- [API Key Setup](#api-key-setup)
- [Architecture](#architecture)
---

### Quick Start

1. Python
   Make sure Python 3.10+ is installed:

```bash
python --version
```

If not installed, download from [Python](https://www.python.org/downloads/)

2. Clone the repository

```bash
git clone repo-url
cd path/to/silicon-valley-trail
```

3. Create and activate a virtual environment

```bash
python -m venv venv
# mac
source venv/bin/activate
# windows
venv\Scripts\activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Set up environment variables
   create .env file in the project root:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

Note:

- The app uses SQLite (no installation required)
- Database is automatically created and seeded on first run (enabled)

6. Run the application

```bash
flask --app game run --port 8000 --debug
```

7. Open in browser

```code
http://127.0.0.1:8000
```

### API Key Setup

This project uses the OpenWeather API to integrate real-world weather into gameplay.

Steps:

1. Create an account on OpenWeather.
2. Generate an API key.
3. Add it to your .env file:

Best Practices

- Never hardcode API keys in source code.
- Never commit .env to GitHub.
- Always use environment variables.

Example .gitignore

```bash
.env
venv/
__pycache__/
*.pyc
instance/
```

You can also use gitignore from [github/gitignore](https://github.com/github/gitignore/tree/main)

#### Running with Mock Data (No API Key Needed)

If you want to run without external API:

Modify config:

```python
USE_MOCK_WEATHER = True
```

Use case :

- uses static weather data
- Avoids API rate limits
- Ideal for testing and demos

## Architecture

The application follows a modular Flask architecture with clear separation of concerns across routing, business logic, persistence, and external integrations.

#### Architecture Layers

- **Frontend (Jinja templates)**: Provides a minimal UI for the game flow, including menu, gameplay, and event screens.
- **Routing Layer (Flask Blueprints)**: Handles HTTP requests, retrieves game state, and delegates logic to the service layer.
- **Service Layer**: Contains core game logic such as action handling, travel progression, event triggering, and win/loss evaluation.
- **Persistence Layer (SQLite + SQLAlchemy)**: Stores the current game session state, including resources, progress, and location.
- **Static Data Layer**: Locations, events, and action effects are defined as Python data structures for fast iteration and easier balancing.
- **External API Integration**: A weather service integrates with the OpenWeather API to influence gameplay (e.g., travel penalties, event conditions), with fallback mock data for reliability.

#### Project Structure

```text
silicon_valley_trail/
│
├── run.py
├── config.py
├── models.py 
├── routes/
│   ├── pages.py
│
├── services/
│   ├── game_engine.py
│   ├── event_service.py
│   ├── weather_service.py 
    |-- save_service.py 
│
├── data/
│   ├── locations.py
│   ├── mock_api_data.py
│
├── tests/
│   ├── test_game.py
│
├── requirements.txt
└── README.md

```

### Dependencies

Main dependencies used in the project

```text
Flask              # Web framework
Flask-SQLAlchemy   # ORM
Flask-Migrate      # Database migrations
Flask-CORS         # Cross-origin support
python-dotenv      # Environment variables
requests           # External API calls
pytest             # Testing framework
pytest-mock        # Mocking support
```

Install all dependencies

```bash
pip install -r requirements.txt
```

### Running Tests

This project uses _pytest_

Run all tests

```bash
pytest
```

Run specific test file

```bash
pytest tests/test-events.py
```

#### AI Usage

**During Development**

AI tools were used to support the development process in the following ways:

- Brainstorming system architecture and application design
- Generating mock data (events, locations)
- Assisting with debugging (Flask routes, state management issues, edge cases)
- Improving documentation clarity and structure
- Suggesting best practices

All AI-generated suggestions were carefully reviewed and validated against trusted sources, including official documentation, technical blogs (e.g., Real Python, freeCodeCamp), and course materials (Coursera, YouTube).

**In Application**

- No AI is directly integrated into the gameplay.
- All game logic, events, and outcomes are deterministic or rule-based.

---

## DESIGN NOTES

### 1. Game Loop and Balance Approach 

Core gameloop is designed around daily turns. On each day player selects an action, the game updates resources, and then checks for travel progress, event triggers, weather effects and win/loss conditions.


### 2. Why OpenWeather API and how it affects gameplay

The game integrates live weather data from a public API. Weather conditions at the player’s current location affect turn outcomes. For example, rain increases travel fatigue, hot temperatures increase coffee consumption, and adverse conditions can reduce progress. If the API is unavailable, the game falls back to cached or mock weather data so gameplay remains functional.

### 3. Data Modeling ( state, events, persistence)


### 4. Error handling (network failures, rate limit) 


### 5. Tradeoffs and if I had more time 

- multiplayer mode and leaderboard 
- more APIs (google maps routes traffic api)
- frontend upgrade (React, styling)
- rate limiting, api versioning 
- session, cookies 
- cache weather for 30mins to use it 
- did not fully normalize events and resources into separate relational tables in the initial version to remove schema complexity