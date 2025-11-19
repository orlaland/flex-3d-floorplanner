This directory is intentionally empty.

To run the FlexPlanner RL agent, copy the FlexPlanner folder from the Thinklab-SJTU/EDA-AI repository into `backend/flexplanner`. The subdirectories (arguments, fp_env, model, policy, etc.) should appear here after copying. Without this code the backend API will fall back to a random policy.

Alternatively, you can add the EDA-AI repository as a Git submodule:

    git submodule add https://github.com/Thinklab-SJTU/EDA-AI.git backend/flexplanner
    git submodule update --init --recursive

Ensure that any use of the original code complies with its licence terms.
