# SQL Query Agent

A LangChain-powered AI agent that converts natural language questions into SQL queries and executes them on a SQLite database.

## Tech Stack
- Python
- LangChain
- OpenAI GPT-4o-mini
- SQLite
- SQLAlchemy

## Features
- Natural Language → SQL
- Read-only database access
- Interactive CLI mode
- Custom database support

## Example Usage

python agent.py --question "Which product generated the highest revenue?"

python agent.py --question "Who are the top 5 customers by spending?"

python agent.py --question "What is the total revenue by product category?"

python agent.py --question "Which country has the most customers?"
