# Backend

This directory contains the backend components for the Flex 3D Floorplanner project.

The backend exposes a simple REST API using FastAPI that wraps the trained reinforcement‑learning policy used to optimise layouts. It is organised as follows:

- **api/** – small FastAPI server exposing `/step` endpoint to apply the RL policy to the current state and return an action.
- **flexplanner/** – placeholder for the FlexPlanner code from the Thinklab‑SJTU/EDA‑AI repository. Due to licensing considerations the code is not included here; please clone it separately into this directory if you wish to train or modify the policy.

## Running the API

1. Install Python dependencies for the API:

    pip install -r backend/api/requirements.txt

2. Start the FastAPI server:

    uvicorn backend.api.main:app --reload --port 8000

This will start a server at `http://localhost:8000`. The frontend can call `/step` on this endpoint to request layout optimisation actions.
