# Geopolitical Strategy Game

_A real-time browser-based strategy game set in 2025, where players assume the role of world leaders aiming to achieve global dominance through financial prowess or military strength._

## Table of Contents

- [Introduction](#introduction)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Game Mechanics](#game-mechanics)
- [Playable Nations & Leaders](#playable-nations--leaders)
- [Military & Economic Power Rankings](#military--economic-power-rankings)
- [Skill Tree Layout](#skill-tree-layout)
- [Diplomacy & Alliances](#diplomacy--alliances)
- [AI Decision Making](#ai-decision-making)
- [Game Events & Reactions](#game-events--reactions)
- [Research & Military Development](#research--military-development)
- [Nuclear War & Endgame Conditions](#nuclear-war--endgame-conditions)
- [Reputation System](#reputation-system)
- [Development & Deployment](#development--deployment)
- [Final Thoughts](#final-thoughts)

---

## Introduction

This game offers a **real-time geopolitical strategy experience**, starting in **January 2025**, where players control major world leaders. The core gameplay revolves around **military expansion, economic development, diplomacy, and global influence**.

Players can leverage **Elon Musk as an AI-driven strategic asset**, research advanced military technologies, form and dissolve alliances, and respond to dynamic global events. The game culminates in either **global peace or total nuclear annihilation**, based on the decisions made by players and AI-controlled nations.

---

## Tech Stack

### Programming Languages & Tools

- **Frontend:**

  - **Vue.js**: For user interface and interactive map components.
  - **MapLibre GL JS**: To render high-performance WebGL-based world maps with smooth zooming and panning.
  - **D3.js**: For visualizing economic data, military statistics, and diplomatic relations.
  - **Chart.js**: For data visualization and statistics.
  - **Turf.js**: For geospatial analysis and operations on map data.

- **Backend:**

  - **Python (FastAPI)**: Handles game logic, AI-driven diplomacy and military strategies.
  - **PostgreSQL**: Stores data on nations, leaders, alliances, and global events.
  - **Redis**: Caches AI computations and game events for efficiency.

- **Game State Management:**

  - **WebSockets**: Ensures real-time updates and interactions.

- **Deployment & Infrastructure:**
  - **Docker & Docker Compose**: Containerization for consistent deployment.
  - **Python Scripts**: Custom deployment, status checking, and reset tools.

---

## Project Structure

```
geopolitics-2025/
├── backend/
│   ├── app.py                      # Main API entry point (FastAPI)
│   ├── requirements.txt            # Python dependencies
│   ├── game_logic/
│   │   ├── __init__.py
│   │   ├── economy.py              # GDP, trade, and financial systems
│   │   ├── military.py             # Military power, research, and warfare mechanics
│   │   ├── diplomacy.py            # AI-driven alliances and diplomatic relations
│   │   ├── nuclear_war.py          # Nuclear warfare logic and consequences
│   │   ├── reputation.py           # Global reputation system
│   │   ├── events.py               # Dynamic world events and triggers
│   │   ├── skill_tree.py           # Skill tree logic and progression
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py               # Database schemas for nations, leaders, and alliances
│   │   ├── queries.py              # Database queries for game state management
│   │   ├── db_config.py            # Database connection configuration
│   │   ├── initialize_all_nations.py # Script to initialize database with nations
│   │   ├── initialize_redis.py     # Script to initialize Redis with game state
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── ai_helpers.py           # AI decision-making utilities
│   │   ├── game_state.py           # Game state management
│   │   ├── websocket_manager.py    # WebSocket connection management
│   ├── tests/
│       ├── __init__.py
│       ├── test_economy.py
│       ├── test_military.py
│       ├── test_diplomacy.py
├── frontend/
│   ├── package.json                # Node.js dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── index.html                  # Entry HTML file
│   ├── src/
│   │   ├── main.js                 # Main entry point
│   │   ├── App.vue                 # Main application component
│   │   ├── assets/                 # Static assets (images, fonts, etc.)
│   │   ├── components/
│   │   │   ├── Map.vue             # Interactive world map component
│   │   │   ├── Dashboard.vue       # Player overview and statistics
│   │   │   ├── Events.vue          # Game notifications and event logs
│   │   │   ├── SkillTree.vue       # Skill tree visualization
│   │   │   ├── Diplomacy.vue       # Diplomacy and alliances visualization
│   │   │   ├── NuclearWar.vue      # Nuclear warfare visualization
│   │   │   ├── Reputation.vue      # Reputation system visualization
│   │   │   ├── UI/                 # Reusable UI components
│   │   ├── views/
│   │   │   ├── GameView.vue        # Main game view
│   │   │   ├── MenuView.vue        # Game menu view
│   │   │   ├── SettingsView.vue    # Settings view
│   │   ├── store/                  # Vuex/Pinia store for state management
│   │   │   ├── index.js
│   │   │   ├── modules/
│   │   │       ├── game.js
│   │   │       ├── nations.js
│   │   │       ├── diplomacy.js
│   │   ├── services/
│   │   │   ├── api.js              # API service for backend communication
│   │   │   ├── websocket.js        # WebSocket service
│   │   ├── router/
│   │       ├── index.js            # Vue Router configuration
│   ├── public/
├── docker/
│   ├── docker-compose.yml          # Docker Compose configuration
│   ├── Dockerfile.backend          # Backend Dockerfile
│   ├── Dockerfile.frontend         # Frontend Dockerfile
├── scripts/
│   ├── deploy.py                   # Deployment script for all components
│   ├── status.py                   # Status checking script
│   ├── reset.py                    # Data reset script
│   ├── README.md                   # Documentation for scripts
├── .gitignore
├── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Git

### Quick Start

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/geopolitics-2025.git
   cd geopolitics-2025
   ```

2. **Install script dependencies**:

   ```bash
   pip install sqlalchemy psycopg2-binary redis requests tabulate
   ```

3. **Deploy all components**:

   ```bash
   python scripts/deploy.py deploy all
   ```

4. **Check the status**:

   ```bash
   python scripts/status.py
   ```

5. **Access the game**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

For more detailed setup instructions, see the [project_setup.md](project_setup.md) file.

---

## Game Mechanics

### 1. Real-Time Gameplay with Adjustable Speed

- Players can **pause, slow down, or accelerate time** to manage events at their preferred pace.
- **Significant events** (e.g., war declarations, major alliances) **automatically pause the game**, prompting player decisions.

### 2. Economy & Trade

- **GDP-based economies** grow through trade, taxation, and strategic investments.
- Nations can **impose sanctions or establish trade agreements** to influence global markets.
- **Arms trade and military support** require logistical planning and time for delivery.

### 3. Military Expansion

- Nations can **research and develop**:
  - **Ground Forces**: Tanks, infantry equipment, logistics vehicles.
  - **Air Force**: Fighter jets, bombers, drones.
  - **Navy**: Battleships, aircraft carriers, submarines.
  - **Defensive Systems**: Anti-missile shields, cyber defense mechanisms.
- **Nuclear weapons** serve as strategic deterrents, with usage leading to severe global consequences.

### 4. Diplomacy & Alliances

- Nations can **form alliances, negotiate treaties, or declare neutrality**.
- **AI reacts dynamically** to player actions, influencing global diplomatic landscapes.
- **Support can be extended or withdrawn**, affecting international relationships and trust.

### 5. Intelligence & Surveillance

- **Elon Musk's Starlink** provides **real-time intelligence** over conflict zones.
- **Spy drones and reconnaissance aircraft** enhance battlefield awareness.
- **Allies react** if intelligence support is modified, impacting trust and cooperation.

---

## Playable Nations & Leaders

| Country            | Leader (January 2025)                            |
| ------------------ | ------------------------------------------------ |
| **United States**  | Donald Trump (AI: Elon Musk as a strategic ally) |
| **China**          | Li Qiang                                         |
| **Russia**         | Vladimir Putin                                   |
| **India**          | Narendra Modi                                    |
| **France**         | Emmanuel Macron                                  |
| **Germany**        | Friedrich Merz                                   |
| **United Kingdom** | Keir Starmer                                     |
| **Poland**         | Sławomir Mentzen                                 |
| **Ukraine**        | Volodymyr Zelenskyy                              |
| **North Korea**    | Kim Jong-un (Unpredictable AI behavior)          |

---

## Military & Economic Power Rankings

- **GDP Rankings:**

  - **United States**: Largest global economy.
  - **China**: Fast-growing economic powerhouse.
  - **Russia**: Weaker economy but resource-rich.

- **Military Power:**

  - **United States**: Dominant global military force.
  - **China/Russia**: Major rivals with significant capabilities.
  - **North Korea**: Nuclear wildcard despite smaller conventional forces.

- **Nuclear Weapons Possession:**
  - **Major Powers**: U.S., Russia, China
  - **Secondary Powers**: UK, France, India
  - **Rogue States**: North Korea

---

## Skill Tree Layout

- **Military Research:**

  - **Ground Forces**: Advanced tanks, mechanized infantry, artillery systems
  - **Air Force**: Stealth aircraft, hypersonic missiles, drone swarms
  - **Navy**: Aircraft carriers, nuclear submarines, autonomous vessels
  - **Space Forces**: Anti-satellite weapons, orbital platforms, space-based defense

- **Economic Development:**

  - **Industry**: Manufacturing efficiency, resource extraction, automation
  - **Technology**: AI research, quantum computing, renewable energy
  - **Infrastructure**: Transportation networks, energy grids, urban development
  - **Trade**: International commerce, financial markets, economic sanctions

- **Intelligence & Cyber:**
  - **Espionage**: Foreign intelligence networks, covert operations, sabotage
  - **Cyber Warfare**: Offensive hacking, defensive systems, information warfare
  - **Surveillance**: Satellite networks, communications monitoring, data analysis
  - **Counter-Intelligence**: Security protocols, counter-espionage, disinformation

---

## Diplomacy & Alliances

- **Alliance Types:**

  - **Military Pacts**: Mutual defense agreements, joint military exercises
  - **Economic Unions**: Free trade zones, customs unions, shared currencies
  - **Intelligence Sharing**: Joint surveillance, shared intelligence assets
  - **Research Cooperation**: Shared technology development, scientific exchange

- **Diplomatic Actions:**

  - **Treaties**: Formal agreements on specific issues (arms control, trade, etc.)
  - **Sanctions**: Economic restrictions to pressure other nations
  - **Aid Packages**: Financial or military assistance to allies or potential allies
  - **Ultimatums**: Final demands before taking more severe action

- **International Organizations:**
  - **United Nations**: Global forum for diplomacy and conflict resolution
  - **Regional Blocs**: NATO, EU, ASEAN, etc. with specific regional interests
  - **Economic Forums**: G7, G20, BRICS for economic coordination
  - **Military Alliances**: Formal defense pacts between multiple nations

---

## AI Decision Making

- AI nations **form alliances, declare wars, and react to world events dynamically**.
- Different AI personalities (**aggressive, diplomatic, opportunistic**) influence behavior.
- AI can **launch nuclear weapons** if national survival is at risk.

---

## Game Events & Reactions

- **Major events** (War Declarations, Alliances, Strategic Deals) trigger automatic game pauses.
- AI reacts to **lost support or betrayal**, allowing rival nations to gain influence.
- **Natural disasters** and **technological breakthroughs** can shift the balance of power.

---

## Research & Military Development

- Military technologies are **researchable** (advanced tanks, aircraft, missile defense systems).
- **Wealthier nations** advance faster in the technology tree.
- **Smaller nations** can catch up through focused investments and strategic alliances.

---

## Nuclear War & Endgame Conditions

- **Limited nuclear war:** Affects regions but allows for recovery.
- **Full-scale nuclear war:** Global catastrophe leading to game over.
- **Global peace:** Achieved through diplomacy and economic stability.

---

## Reputation System

- **Global Reputation Score:** Determines trust levels among nations.
- **Breaking alliances, war declarations, and nuclear strikes impact reputation.**
- **Media and public perception influence diplomatic relations.**

---

## Development & Deployment

### Deployment Scripts

The project includes several scripts to simplify deployment and management:

1. **Deploy Script** (`scripts/deploy.py`):

   ```bash
   # Deploy all components
   python scripts/deploy.py deploy all

   # Deploy specific components
   python scripts/deploy.py deploy database
   python scripts/deploy.py deploy redis

   # Stop all containers
   python scripts/deploy.py stop
   ```

2. **Status Script** (`scripts/status.py`):

   ```bash
   python scripts/status.py
   ```

3. **Reset Script** (`scripts/reset.py`):

   ```bash
   # Reset all game data
   python scripts/reset.py all

   # Reset specific components
   python scripts/reset.py database
   python scripts/reset.py redis
   ```

### Database Configuration

- **PostgreSQL**: Runs on port 5433, with username/password: admin/admin
- **Redis**: Runs on port 6379

For more details on development and deployment, see the [scripts/README.md](scripts/README.md) file.

---

## Final Thoughts

This project aims to create a deep, strategic, and reactive geopolitical simulation where no two games play the same. The real-time AI-driven diplomacy and military strategy ensure that players must balance power, reputation, and risk to succeed.
