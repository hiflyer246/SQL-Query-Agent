# SQL Query Agent

A LangChain-powered AI agent that converts natural language questions into SQL queries and executes them on a SQLite database.

## Tech Stack

- Python
- LangChain
- OpenAI GPT-4o-mini
- SQLite

## Features

- Natural Language → SQL Query Generation
- Read-only database access by default
- Interactive command-line interface
- Support for custom SQLite databases
- AI-powered query understanding and execution

## Installation

```bash
git clone https://github.com/yourusername/SQL-Query-Agent.git
cd SQL-Query-Agent

pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run with the demo database:

```bash
python agent.py
```

Ask a single question:

```bash
python agent.py --question "Which product generated the highest revenue?"
```

Use a custom database:

```bash
python agent.py --db mydatabase.sqlite
```

## Sample Questions

- Which product generated the highest revenue?
- Who are the top 5 customers by spending?
- What is the total revenue by product category?
- Which country has the most customers?
- Which customers purchased a specific product?
- What are the monthly sales trends?
- Which products have the lowest stock levels?
- What is the average order value?
- Show all orders placed in April 2025.
- Which customer placed the most orders?

## Project Structure

```text
SQL-Query-Agent/
│
├── agent.py
├── requirements.txt
├── README.md
├── .env
```

## Future Improvements

- Streamlit web interface
- Support for PostgreSQL and MySQL
- Query history and logging
- SQL query visualization
- Multi-database support
