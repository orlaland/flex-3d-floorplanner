from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Add flexplanner to sys.path so we can import the policy code if available
import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FLEXPLANNER_DIR = ROOT / "flexplanner"
if FLEXPLANNER_DIR.exists():
    sys.path.append(str(FLEXPLANNER_DIR))

# Placeholder for policy loading; update this to load a trained policy
# from policy.load_policy import load_trained_policy
# policy = load_trained_policy(checkpoint_path)

app = FastAPI()

class State(BaseModel):
    values: List[float]

class Action(BaseModel):
    idx: int
    dx: float
    dz: float
    dtheta: float

@app.get("/")
def root():
    return {"status": "ok", "message": "FlexPlanner API running"}

@app.post("/step", response_model=Action)
def flexplanner_step(state: State):
    # TODO: Replace with real policy inference.
    import random
    num_objects = len(state.values) // 4
    idx = random.randint(0, num_objects - 1) if num_objects > 0 else 0
    dx = (random.random() - 0.5) * 0.2
    dz = (random.random() - 0.5) * 0.2
    dtheta = (random.random() - 0.5) * 0.5
    return Action(idx=idx, dx=dx, dz=dz, dtheta=dtheta)
