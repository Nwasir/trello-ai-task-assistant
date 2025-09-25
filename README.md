Trello AI Task Assistant
Overview

The Trello AI Task Assistant is a Streamlit app that helps users turn high-level tasks into structured subtasks using AI. It can automatically send generated subtasks to a Trello board, streamlining task management and improving productivity.

This project was created for an AI Implementation Challenge to demonstrate practical AI integration in a real SaaS workflow.

Key Features

Generate subtasks from a single high-level task using Hugging Face AI.

Directly create Trello cards in your chosen board and list.

Interactive Streamlit UI for easy input, editing, and task management.

Ready for Streamlit Cloud deployment with secure secrets.

Demo

Live app: [Insert Streamlit App URL]

Loom walkthrough: [Insert Loom Link]

Quick Setup

Clone the repo:

git clone <your-repo-url>
cd trello-ai-task-assistant


Create and activate a Python environment:

python3 -m venv my_project_env
source my_project_env/bin/activate


Install dependencies:

uv add -r pyproject.toml
# or pip install -r requirements.txt


Set up Hugging Face and Trello credentials in Streamlit secrets.

Usage

Enter a task in the Streamlit app.

Click Generate Suggestions to get AI-generated subtasks.

Select a Trello board and list.

Click Send Subtasks to Trello to create cards.

Tech Stack

Streamlit → UI

Hugging Face Transformers → AI subtasks generation

Trello API → Task automation

Python → Backend logic

Project Structure
trello-ai-task-assistant/
├── app/app.py           # Streamlit app
├── .env.example         # Placeholder secrets
├── plan.md              # Project plan
├── README.md            # This README
├── pyproject.toml       # Dependencies
└── requirements.txt
