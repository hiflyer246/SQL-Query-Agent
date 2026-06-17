"""
SQL Query Agent using LangChain.

Connects to a SQLite database and answers natural language questions
by generating and executing SQL queries.

Usage:
    python agent.py                          # uses demo database
    python agent.py --db path/to/db.sqlite   # your database
    python agent.py --db mydb.sqlite --question "How many users signed up last month?"
"""

import argparse
import os
import sqlite3
from urllib.parse import quote
import sys
import openai

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

load_dotenv()

def create_demo_database(db_path: str):
    """Creates a demo AI SaaS business SQLite database for testing."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            country TEXT,
            created_at DATE DEFAULT CURRENT_DATE
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            order_date DATE DEFAULT CURRENT_DATE
        );

        DELETE FROM orders;
        DELETE FROM products;
        DELETE FROM customers;

        INSERT INTO customers VALUES
        (1,'Emma Wilson','emma@techvision.ai','USA','2025-01-10'),
        (2,'Raj Patel','raj@smartanalytics.io','India','2025-01-15'),
        (3,'Sophia Chen','sophia@cloudmatrix.com','Singapore','2025-02-02'),
        (4,'Michael Brown','michael@databridge.ai','Canada','2025-02-08'),
        (5,'Ava Johnson','ava@futureml.com','USA','2025-02-15'),
        (6,'Arjun Mehta','arjun@neuralworks.ai','India','2025-03-01'),
        (7,'Lucas Martin','lucas@insightlabs.io','UK','2025-03-12'),
        (8,'Olivia Taylor','olivia@aiflow.com','Australia','2025-03-25'),
        (9,'Daniel Kim','daniel@vectordb.ai','South Korea','2025-04-01'),
        (10,'Isabella Garcia','isabella@cognify.ai','Spain','2025-04-07');

        INSERT INTO products VALUES
        (1,'AI Chat API','AI Services',499.99,500),
        (2,'Vector Database Service','Cloud Services',299.99,300),
        (3,'RAG Enterprise Platform','AI Services',1299.99,100),
        (4,'Model Monitoring Suite','MLOps',899.99,150),
        (5,'Prompt Engineering Toolkit','Developer Tools',199.99,400),
        (6,'LLM Analytics Dashboard','Analytics',799.99,120),
        (7,'Document Intelligence API','AI Services',699.99,250),
        (8,'ML Deployment Manager','MLOps',999.99,90);

        INSERT INTO orders VALUES
        (1,1,1,2,999.98,'2025-04-01'),
        (2,2,2,1,299.99,'2025-04-02'),
        (3,3,3,1,1299.99,'2025-04-03'),
        (4,4,4,1,899.99,'2025-04-04'),
        (5,5,5,3,599.97,'2025-04-05'),
        (6,6,6,1,799.99,'2025-04-06'),
        (7,7,7,2,1399.98,'2025-04-07'),
        (8,8,8,1,999.99,'2025-04-08'),
        (9,9,1,1,499.99,'2025-04-09'),
        (10,10,3,1,1299.99,'2025-04-10'),
        (11,2,4,1,899.99,'2025-04-11'),
        (12,6,2,2,599.98,'2025-04-12'),
        (13,1,7,1,699.99,'2025-04-13'),
        (14,4,5,4,799.96,'2025-04-14'),
        (15,8,6,1,799.99,'2025-04-15'),
        (16,3,1,2,999.98,'2025-04-16'),
        (17,5,8,1,999.99,'2025-04-17'),
        (18,7,3,1,1299.99,'2025-04-18'),
        (19,9,4,1,899.99,'2025-04-19'),
        (20,10,7,1,699.99,'2025-04-20');
    """)

    conn.commit()
    conn.close()


def sqlite_uri(db_path: str, read_only: bool = True) -> str:
    abs_path = os.path.abspath(db_path)
    if read_only:
        return f"sqlite:///file:{quote(abs_path)}?mode=ro&uri=true"
    return f"sqlite:///{abs_path}"


def build_agent(db_path: str, read_only: bool = True):
    db = SQLDatabase.from_uri(sqlite_uri(db_path, read_only=read_only))
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )
    return agent, db


def main():
    parser = argparse.ArgumentParser(description="SQL Query Agent")
    parser.add_argument("--db", default="demo.sqlite", help="SQLite database path")
    parser.add_argument("--question", help="Natural language question (omit for interactive)")
    parser.add_argument("--allow-write", action="store_true", help="Open the SQLite database read-write instead of read-only")
    args = parser.parse_args()

    if args.db == "demo.sqlite" and not os.path.exists("demo.sqlite"):
        print("🏗️  Creating demo e-commerce database...")
        create_demo_database("demo.sqlite")

    agent, db = build_agent(args.db, read_only=not args.allow_write)
    print(f"\n📊 Connected to: {args.db}")
    print(f"🔒 Mode: {'read-write' if args.allow_write else 'read-only'}")
    print(f"📋 Tables: {', '.join(db.get_table_names())}\n")

    if args.question:
        print(f"❓ Question: {args.question}")
        try:
            result = agent.invoke({"input": args.question})
            print(f"\n✅ Answer: {result['output']}")
        except openai.RateLimitError as e:
            print("\n⚠️ OpenAI quota exceeded or rate-limited. Check your API plan/billing and try again.")
            print(f"Details: {e}")
            sys.exit(1)
        except Exception as e:
            print("\n❗ An error occurred while invoking the agent:")
            print(e)
            sys.exit(1)
    else:
        print("💬 SQL Agent ready. Ask questions in natural language. Type 'quit' to exit.\n")
        while True:
            question = input("You: ").strip()
            if question.lower() in ("quit", "exit", "q"):
                break
            if not question:
                continue
            try:
                result = agent.invoke({"input": question})
                print(f"\nAgent: {result['output']}\n")
            except openai.RateLimitError as e:
                print("\n⚠️ OpenAI quota exceeded or rate-limited. Check your API plan/billing and try again.")
                print(f"Details: {e}\n")
                break
            except Exception as e:
                print("\n❗ An error occurred while invoking the agent:")
                print(e)
                break


if __name__ == "__main__":
    main()
