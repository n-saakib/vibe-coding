# AGENT.md - Project Mandates & Instructions

This file contains the core mandates and instructions for the Gemini CLI agent. It must be followed strictly and updated as the project evolves.

## Core Rules
1. **Atomic Commits:** Commit after every small functional increment or logical change.
2. **Documentation:**
   - Maintain `docs/architecture.md` (high-level design, components).
   - Maintain `docs/behavior.md` (user flow, state transitions, game logic).
   - Maintain `README.md` (project overview, setup, features).
3. **Life Journal:**
   - Maintain `JOURNAL.md` as a comprehensive project diary.
   - Document every success, mistake, decision, fix, and plan.
   - It should be a complete journey of the project from beginning to end.
4. **Environment:**
   - Always use the Python virtual environment (`venv`) for all operations (installing packages, running tests, etc.).
5. **Context Management:**
   - Always keep this `AGENT.md` file in context.
   - Update it whenever rules or plans change.

## Technical Stack
- **Language:** Python 3.x
- **GUI Library:** Pygame
- **Architecture:** Model-View-Controller (MVC)

## Feature Requirements
- **Multiplayer:** 2 players offline on the same PC.
- **Single Player:** 1 player vs AI.
- **AI Modes:**
  - Easy (Random moves).
  - Hard (Minimax algorithm).

## Phase 1 Plan: Model Development
- Define the board state and representation.
- Implement move logic and win/draw detection.
- Unit tests for game logic.
