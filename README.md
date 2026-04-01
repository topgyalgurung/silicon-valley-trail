# SILICON VALLEY TRAIL

## Overview

Silicon Valley Trail is a replayable, Oregon Trail–inspired simulation game where you lead a startup team from San Jose to San Francisco. Each turn, you make strategic decisions to manage limited resources while navigating dynamic events and weather-driven challenges.

The game blends deterministic logic with randomness and real-time weather data to create a balanced and engaging experience. Built with a modular Flask architecture, the project focuses on clean design, scalability, and testability.

## Project Links

- **Live Demo:** [Open app](<[https://...](https://silicon-valley-trail.onrender.com/)>)
- **Demo Video:** [Watch here](<[https://...](https://drive.google.com/file/d/1e_DFbQ7lJ1KUc2DEPLHkedoMEOTIUcFM/view?usp=sharing)>)

## Table of Contents

1. [Quick Start](#quick-start)
2. [API Key Setup](#api-key-setup)
   - [Running with Mock Data (No API Key Needed)](#running-with-mock-data-no-api-key-needed)
3. [Architecture](#architecture)
   - [Architecture Layers](#architecture-layers)
   - [Project Structure](#project-structure)
   - [Dependencies](#dependencies)
   - [Tech Stack](#tech-stack)
4. [Running Tests](#running-tests)
5. [Example Commands / Inputs](#example-commands--inputs)
   - [Run the game locally](#run-the-game-locally)
   - [Sample gameplay flow](#sample-gameplay-flow)
   - [Example input sequence](#example-input-sequence)
6. [AI Usage](#ai-usage)
7. [Design Notes](#design-notes)
   - [Game Loop and Balance Approach](#1-game-loop-and-balance-approach)
   - [Why OpenWeather API and How It Affects Gameplay](#2-why-openweather-api-and-how-it-affects-gameplay)
   - [API Choice and Gameplay Impact](#api-choice-and-gameplay-impact)
   - [Data Modeling (State, Events, Persistence)](#3-data-modeling-state-events-persistence)
   - [Error Handling (Network Failures, Rate Limits)](#4-error-handling-network-failures-rate-limits)
   - [Tradeoffs and If I Had More Time](#5-tradeoffs-and-if-i-had-more-time)
     - [Tradeoffs](#tradeoffs)
     - [If I Had More Time](#if-i-had-more-time)

### Quick Start

1. Python
   Make sure Python 3.10+ is installed:

   ```bash
   python --version
   ```

   If not installed, download from [Python](https://www.python.org/downloads/)

2. Clone the repository

   ```bash
   git clone <repo-url>
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
   create `.env` file in the project root:

   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

   Note:
   - The app uses SQLite (no installation required).
   - To use a different database, add DATABASE_URL to your .env file
   - Database is automatically created and seeded on first run

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

Benefits:

- uses static weather data
- Avoids API rate limits
- Ideal for testing and demos

## Architecture

The application follows a modular Flask architecture with clear separation of concerns across routing, business logic, persistence, and external integrations. It uses [Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) and [Flask Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/) to keep the codebase organized, maintainable, and easier to scale.

This structure also improves testability by allowing components to be initialized, isolated, and tested independently.

#### Architecture Layers

- **Frontend (Jinja)**: Renders game UI (menu, gameplay, events)
- **Routing (Flask Blueprints)**: Handles requests and delegates to services
- **Service Layer**: Core game logic (actions, progression, events, win/loss)
- **Persistence (SQLite + SQLAlchemy)**: Stores game state and resources
- **Static Data**: Defines locations, events, and action effects
- **External API**: Weather integration (OpenWeather) with mock fallback for reliability

#### Project Structure

```text
silicon-valley-trail/
│
├── data/
│   ├── mock_api_data.py      # Mock weather, events, initial state
│   └── seed_data.py          # Database seeding (locations)
│
├── game/
│   ├── __init__.py           # App factory
│   │
│   ├── errors/
│   │   ├── __init__.py
│   │   └── handlers.py       # Error handling (404, etc.)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py         # SQLAlchemy models (GameSession, Location)
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── pages.py          # HTTP routes / controllers
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── game_service.py   # Core game logic
│   │   ├── event_service.py  # Event handling logic
│   │   ├── weather_service.py# Weather API + mock fallback
│   │   └── result_types.py   # Shared result/response structures
│   │
│   ├── templates/            # Jinja templates (UI)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── state.py          # Game state helpers
│   │   └── utils.py          # Utility functions
│
├── tests/                    # Pytest test suite
├── .env.example              # Example environment variables
├── requirements.txt
├── run.py                    # Entry point
└── README.md

```

### Dependencies

#### Tech Stack

- **Frontend**: Jinja2 (server-rendered UI)
- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite (default), configurable via `DATABASE_URL`
- **External API**: OpenWeather (weather-driven gameplay)
- **Testing**: Pytest

#### Dependencies

- Flask — web framework
- Flask-SQLAlchemy — ORM for database interactions
- Flask-Migrate — database migrations
- Flask-CORS — cross-origin support
- python-dotenv — environment variable management
- requests — HTTP client for external API calls

**Testing**

- pytest — testing framework
- pytest-mock — mocking utilities

### Running Tests

This project uses **pytest** for unit testing.

Run all tests

```pytest
pytest
```

Run specific test file

```bash
pytest tests/test_events.py
```

Run with verbose output

```bash
pytest -v
```

Note:

- Tests are isolated and do not depend on external APIs (mock data is used)
- Ensure your virtual environment is activated before running test

### Example Commands / Inputs

Because this game uses a browser UI, the main player inputs are button clicks rather than typed commands. The example below shows both how to launch the app and what a typical gameplay sequence looks like.

This sample uses mock weather data so it works without an API key. Exact events may vary because location events are semi-random.

#### Run the game locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app game run --port 8000 --debug
```

Open `http://127.0.0.1:8000` in your browser.

#### Sample gameplay flow

1. Click `New Game`
2. On Day 1 in `San Jose`, click `Travel to next location`
3. The team moves to `Santa Clara`
4. Travel consumes resources, weather effects are applied, and a location event appears
5. If the event is `Discount Coffee Cart`, click `Buy extra coffee`
6. Return to the main game screen and click `Work on product`
7. This reduces `bugs`, consumes `coffee`, lowers `morale`, and advances the day
8. On the next turn, click `Rest and recover`
9. This restores `morale`, uses some `coffee`, and advances the day
10. Click `Travel to next location` again to move to `Sunnyvale`
11. A new event appears based on the location, current game state, and API/weather data
12. Continue choosing between `Travel to next location`, `Rest and recover`, `Work on product`, and `Marketing push` until you either reach `San Francisco` or lose by running out of time or resources

#### Example input sequence

`New Game` -> `Travel to next location` -> `Buy extra coffee` -> `Work on product` -> `Rest and recover` -> `Travel to next location` -> `Pitch immediately` -> `Marketing push`

This sequence demonstrates the core game loop:

- choose one action per turn
- spend or recover resources
- move between real Silicon Valley locations
- resolve a semi-random event after travel
- make tradeoff decisions that affect future turns

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

## DESIGN NOTES

### 1. Game Loop and Balance Approach

**Game Loop**

- The game is played in daily turns, with a total limit of 20 days to reach San Francisco
- The journey is structured across 12 real-world locations seeded into the database
- Each turn, the player chooses one action such as travel, rest, work, or marketing
- Actions update core resources: cash, morale, coffee, hype, and bugs
- Choosing `travel` moves the player to the next location, updates progress, applies weather-related logic, and may trigger a location-based event
- After every turn, the system re-evaluates win and loss conditions

**Balance Approach**

- The game is designed around tradeoffs rather than optimal single-step choices
- Short-term gains, such as earning cash or increasing hype, can also increase risk through bugs, morale loss, or resource drain
- Recovery actions improve stability but cost time and slow progress
- The 20-day limit adds pressure and forces the player to balance momentum with survival
- This creates a simple but meaningful decision loop where poor resource management or delayed progress can lead to failure

### 2. Why OpenWeather API and How It Affects Gameplay

I chose the OpenWeather API because it was lightweight to integrate, practical within the project timeline, and able to influence gameplay in a meaningful way. Instead of using external data only for display, I used weather conditions as an input into backend game logic

**Why this API**

- It was simple to integrate within a short development timeline
- It adds real-world variability to the game
- It fits naturally with the project’s location-based travel structure

**Gameplay Impact**

- Weather is fetched for the player’s current location
- Conditions such as `Rain`, `Fog`, or `Clear` can influence gameplay effects and event eligibility
- This makes each run feel less predictable while still keeping the game rule-based and testable

**Reliability**

- The application includes fallback and mock weather data so gameplay remains functional if the live API is unavailable
- This prevents the weather integration from becoming a single point of failure

### 3. Data Modeling (State, Events, Persistence)

The data model was designed to keep the game state simple, explicit, and easy to update on each turn.

![Database Design](static/images/database-design.png)

**State**

- A `GameSession` represents a single run of the game
- It stores the player’s evolving state, including the current location, destination, current day, distance traveled, progress, and core resources such as cash, morale, coffee, hype, and bugs
- It also stores status fields used to determine whether the player is still in progress, has won, or has lost

**Events**

- Events are defined as structured Python mock data rather
  than database tables
- Each location has its own set of event definitions, making it easier to customize gameplay by city
- Events can apply direct effects or present player choices with different outcomes
- Keeping events in data structures made iteration faster during balancing and development

**Persistence**

- Game state is persisted in SQLite using SQLAlchemy ORM
- The `Location` table stores the 12 seeded real-world locations used in the journey
- The `GameSession` table stores the active game state so progress can be tracked across requests
- This separation keeps static reference data (locations) distinct from dynamic gameplay state (session/resources/progress)

This design made it easier to reason about the system, test components independently, and update game state consistently after each turn.

### 4. Error Handling (Network Failures, Rate Limits)

The application is designed to fail gracefully so the game remains playable even when external services are unavailable.

**Weather / External API Handling**

- The weather service handles timeouts, network failures, and unexpected API responses
- If a live weather request fails, the application falls back to mock or default weather data
- This prevents the weather API from becoming a single point of failure during gameplay
- Mock mode is also supported for local development and testing

**Application-Level Error Handling**

- Flask error handlers are used to return user-friendly responses for common failures such as `404` and `500`
- Routes validate player input, such as invalid actions or missing event choices, and return appropriate error responses
- This helps protect the application from invalid requests while keeping behavior predictable

**Development Support**

- Debug mode is enabled during development to make local troubleshooting easier
- In production, this would be disabled in favor of safer runtime configuration

### 5. Tradeoffs and if I had more time

#### Tradeoffs

- I limited the project to a single external API so I could keep integration complexity manageable and ensure the core backend logic remained reliable.
- I stored events as structured Python data rather than normalized database tables to prioritize development speed and simpler iteration during balancing.
- I kept weather effects intentionally lightweight so external data could influence gameplay without dominating the main turn-based decision logic.

#### If I Had More Time

**Gameplay & UI**

- Improve the UI/UX with more polished styling and clearer gameplay feedback
- Integrate additional APIs, such as Google Maps Routes for travel/traffic data and Eventbrite, Meetup, or Luma for real-world event inspiration, to make gameplay more dynamic and location-aware
- Expand test coverage for core game logic and edge cases

**Backend & System Design**

- Refactor event and resource handling into more structured schemas for easier scaling and maintenance
- Strengthen the service layer and request flow to make responsibilities even clearer between routes, business logic, and persistence

**Reliability & Performance**

- Implement simple caching for weather data to reduce repeated external requests
- Add structured logging for easier debugging and better observability
- Improve network resilience with clearer timeout and fallback behavior
- Add integration tests to validate end-to-end gameplay flows
