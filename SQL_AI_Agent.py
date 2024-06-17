import logging
import os
import duckdb
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()
Groq.api_key = os.getenv('GROQCLOUD_API_KEY')

logging.basicConfig(filename='error.log', level=logging.ERROR)

def english_to_sql(question):
    try:
        response = Groq.generate(
            model="DuckDB-NSQL-7B",
            prompt=f"Convert this question to SQL: {question}"
        )
        sql_query = response['generated_text'].strip()
        return sql_query
    except Exception as e:
        raise RuntimeError(f"Failed to convert question to SQL: {e}")

def execute_sql_query(sql_query):
    try:
        result = sql_query.execute().fetchall()
        return result
    except Exception as e:
        raise RuntimeError(f"Failed to execute SQL query: {e}")

def english_to_sql(question):
    regex = re.compile(r"What is the (.*)?")
    match = regex.match(question)
    if match:
        return f"SELECT {match.group(1)} FROM orders"
    return None

if __name__ == '__main__':
    print("Welcome to the LLM-powered Q&A agent. Ask your questions about the Northwind database.")
    db_connection = duckdb.connect(database='northwind.db')
    while True:
        question = input("Your question: ")
        if question.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        try:
            sql_query = english_to_sql(question)
            print(f"Generated SQL Query: {sql_query}")
            if sql_query:
                sql_query = english_to_sql(question)
                print(f"Generated SQL Query: {sql_query}")
                results = execute_sql_query(sql_query)
                print("Results:")
                for row in results:
                    print(row)
            else:
                results = db_connection.execute(sql_query).fetchall()
                print("Results:")
                for row in results:
                    print(row)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")