# Flex 3D Floorplanner

This repository stitches together an interactive 3D viewer with a deep‑reinforcement‑learning (RL) back‑end to explore **flexible 3D floorplanning**, inspired by the NeurIPS 2024 paper **“FlexPlanner: Flexible 3D Floorplanning via Deep Reinforcement Learning in Hybrid Action Space with Multi‑Modality Representation.”**

## Overview

The goal of this project is to allow you to load your own 3D objects (e.g. furniture, NFTs, CAD parts) into a browser‑based viewer and then automatically arrange them within a bounded room using a trained RL policy.  The RL agent seeks to maximise space utilisation while minimising collisions or other constraint violations, following the reward formulation described in the paper.  A baseline “greedy” layout and a random layout are also provided so you can compare performance.

The repository is organised as follows:

| Path | Description |
|------|-------------|
| `frontend/` | Contains the React + Three.js source code for the viewer.  You will need to copy your own viewer components here (e.g. `Portfolio3DViewer.tsx`, `ObjModelViewer.tsx`).  A guide is provided to help you expose a state vector, call the RL API and apply the returned actions. |
| `backend/` | A Python back‑end built with FastAPI that wraps the FlexPlanner policy.  The `api/` directory exposes a `/step` endpoint that accepts the current layout state and returns an action.  The `flexplanner/` directory is **intentionally left empty** – you must populate it with the `FlexPlanner` implementation from the original authors (see below). |

## Getting Started

### 1.  Populate the FlexPlanner code

The FlexPlanner implementation is distributed under the MIT licence by the original authors.  To run the RL policy you must copy the `FlexPlanner` folder from [Thinklab‑SJTU/EDA‑AI](https://github.com/Thinklab-SJTU/EDA-AI) into `backend/flexplanner/` in this repo.  The recommended way is to clone their repository and copy the `FlexPlanner` subdirectory:

```bash
git clone https://github.com/Thinklab-SJTU/EDA-AI.git
cp -r EDA-AI/FlexPlanner <path-to-this-repo>/backend/flexplanner
```

Alternatively, you may add the original repository as a Git submodule in this directory.

### 2.  Run the backend API

Create a Python virtual environment, install requirements, and start the FastAPI server:

```bash
cd backend/api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r ../flexplanner/requirements.txt  # install FlexPlanner dependencies
uvicorn main:app --reload --port 8000
```

This will start the API on `http://localhost:8000`.  You can test it with a POST request:

```bash
curl -X POST http://localhost:8000/step \ 
     -H "Content-Type: application/json" \ 
     -d '{"values":[0.5,0.5,0.2,0.2]}'
```

When properly wired up, the API will use the loaded FlexPlanner policy to choose the index of a block to move and the relative translation/rotation increments.

### 3.  Implement the front‑end integration

The `frontend/` directory should house your React/TypeScript code.  At a high level you need to:

1. **Build a state vector** representing your current layout.  Each object should contribute its x‑position, z‑position, width and depth, normalised to the room dimensions.  For example:

   ```ts
   function buildState(objects: THREE.Object3D[], room: THREE.Box3): number[] {
     const state: number[] = [];
     const roomSizeX = room.max.x - room.min.x;
     const roomSizeZ = room.max.z - room.min.z;
     objects.forEach(o => {
       const box = new THREE.Box3().setFromObject(o);
       const centre = box.getCenter(new THREE.Vector3());
       const size = box.getSize(new THREE.Vector3());
       state.push(
         (centre.x - room.min.x) / roomSizeX,
         (centre.z - room.min.z) / roomSizeZ,
         size.x / roomSizeX,
         size.z / roomSizeZ
       );
     });
     return state;
   }
   

2. **Call the API** with this state to obtain an action.  Use `fetch` or `axios` to POST the `values` array to `http://localhost:8000/step`.

3. **Apply the action** to your scene.  The returned JSON has the structure `{ idx, dx, dz, dtheta }`, indicating which object to move and by how much (normalised to room dimensions).

4. **Recompute metrics** (collisions, space efficiency, reward) after applying the action and re‑render your scene.  Optional: show these metrics in your UI as done in the NeurIPS paper.

See the comments in `backend/api/main.py` and the algorithms in the FlexPlanner paper for further guidance.

### 4.  Train or load a policy

By default `main.py` uses a placeholder random policy.  Once the FlexPlanner environment is in place you can load a pre‑trained policy checkpoint using functions in `backend/flexplanner/policy/load_policy.py` (see the original repository for details).  Alternatively, you can train your own RL policy using the scripts provided in the FlexPlanner repository.  Training may require a GPU and some time.

## Contributing

This project is provided as a starting point for experimentation and learning.  Contributions are welcome – whether improving the API wrapper, adding better visualisations or integrating other RL algorithms.  Please respect the licences of the original FlexPlanner authors when copying their code.
