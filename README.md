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

The application follows a modular Flask architecture with clear separation of concerns across routing, business logic, persistence, and external integrations with [Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) and [Flask Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/) with the goal of making it more maintainable and organized. This will also help write tests easier and also test each component independently.

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

#### Flask App structure 

Blueprints
- 

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

The core game loop is designed around daily turns. On each day, the player selects an action, which updates resources such as cash, morale, coffee, hype, and bugs. If the player chooses to travel, the game moves to the next location, applies weather effects, and triggers an event. After each turn, the system checks win/loss conditions.
The balance is designed around tradeoffs:

- short-term gains (e.g., hype, cash) often increase risk (e.g., bugs, morale loss)
- recovery actions improve stability but slow momentum.

### 2. Why OpenWeather API and how it affects gameplay

I used the OpenWeather API because it is simple to integrate, reliable, and provides real-time weather data (e.g., weather conditions and temperature). It also has a generous free tier, which makes it suitable for rapid prototyping within a short timeframe.

The goal was to include an external API that meaningfully impacts gameplay rather than just displaying information.

The game integrates live weather data from a public API. Weather conditions at the player’s current location affect turn outcomes. For example, rain increases travel causing morale loss, hot temperatures increase coffee consumption. If the API is unavailable, the game falls back to mock weather data so gameplay remains functional (cache weather data was not implemented)

1. Passive Effects (Consistent Impact)
   Each turn, the current weather applies small effects to the team’s resources. This creates a predictable baseline challenge that players must manage
2. Conditional Events
   Some events are only triggered under specific weather conditions. Example a bad commute appears during rain.

Approach:

To keep the system clean and maintainable, API data is normalized into a simple structure (e.g., weather_main, temperature) before being used in game logic. This avoids tight coupling to raw API responses and makes the system easier to test and extend.

### 3. Data Modeling ( state, events, persistence)

The game state is stored in a GameSession model, which tracks core resources (cash, morale, coffee, hype, bugs), current location, and game status.

Locations are stored in a separate table and define the travel path from start to destination.
Events are defined as structured data (Python dictionaries) grouped by location. Each event includes:

- metadata (id, name, description)
- optional conditions (e.g., bugs threshold, API conditions)
- multiple choices with resource tradeoffs

This approach keeps the system flexible and easy to modify without requiring frequent database schema changes. Game state is persisted using a relational database (SQLite with SQLAlchemy), allowing sessions to be saved and resumed.

### 4. Error handling (network failures, rate limit)

The game is designed to remain stable even if the API fails.

If the weather API is unavailable:
- the system falls back to default or mock data
- weather-dependent events are skipped
- normal gameplay continues without interruption

This ensures the game remains playable and avoids blocking core functionality due to external dependencies.

Error Handling in Flask App 

Debug Mode
- enable debug mode Flask outputs a really nice debugger directly on your browser during development. First set your app environment
```bash
$ export FLASK_APP=game
```
- then enable debug mode  
```bash
$ export FLASK_DEBUG=1 
```

Custom error pages:
To declare a custom error handler, the @errorhandler decorator is used


### 5. Tradeoffs and if I had more time

Tradeoffs

- Using a single API kept the implementation simple and reliable within the time constraint
- Events are stored as in-code data rather than fully normalized database tables to reduce complexity
- Weather effects are intentionally lightweight to avoid overly punishing gameplay

**If I Had More Time:**

- Add multiplayer mode and leaderboard
- deployment to cloud, CI/CD deployment testing pipelines
- Integrate additional APIs (e.g., traffic data, startup/news sentiment)
- Improve styling and frontend using React and modern UI components
- Implement caching for API responses (e.g., 30-minute weather cache)
- Add rate limiting and API versioning
- Improve session management (cookies, authentication)
- Normalize events and resources into separate relational tables for scalability
