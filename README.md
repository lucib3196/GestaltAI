
# Project Setup & Installation
This project uses Poetry for dependency management and runs both a LangGraph dev server and a Streamlit.

## Installation
1. Install dependencies (root)
From the root directory of the project:
```bash
poetry install

```

2. Install dependencies (app directory)
There is a known Poetry configuration quirk where dependencies must also be installed inside the app/ directory. 

Although both installs reference the same package set, both are required for the project to function correctly (This is so deployment works)

```bash
cd app
poetry install
```

3. (Recommended) Activate the Poetry shell
Activating the Poetry shell makes commands shorter and easier to run: (Might need to be installed)
```bash
poetry shell
```

if you do not activate the shell, you must prefix all commands with:

```bash
poetry run <command>
```

## Running Application


1. Start the LangGraph dev server
from the `app/` directory

```bash
langgraph dev --config langgraph.json
```

2. Start the streamlit app
In a separate terminal:
```bash
streamlit run streamlit_app/main.py
```
## Notes & Troubleshooting
- The Streamlit UI may not render immediately if the LangGraph server is not running.
- You’ll know the LangGraph server is working when:
    A LangGraph dev popup appears, and/or
    You are prompted to sign in or authenticate
If you are asked to log in and run into issues, just ask me and I’ll help you get through it.


## Summary

```bash
# Install
poetry install
cd app && poetry install

# Optional but recommended
poetry shell

# Run backend
langgraph dev --config langgraph.json

# Run frontend (seperate terminal)
streamlit run streamlit_app/main.py
```