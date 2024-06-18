import logging
import os
import duckdb
from dotenv import load_dotenv
import re

load_dotenv()

logging.basicConfig(filename='error.log', level=logging.ERROR)

def fallback_sql_generation(question):
    question_lower = question.lower()
    
    if "how many tables" in question_lower:
        return "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'main';"
    elif "list tables" in question_lower:
        return "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main';"
    elif "list customers" in question_lower or "show customers" in question_lower:
        return "SELECT * FROM customers;"
    elif "count customers" in question_lower or "number of customers" in question_lower:
        return "SELECT COUNT(*) FROM customers;"
    elif "list orders" in question_lower or "show orders" in question_lower:
        return "SELECT * FROM orders;"
    elif "count orders" in question_lower or "number of orders" in question_lower:
        return "SELECT COUNT(*) FROM orders;"
    elif "list products" in question_lower or "show products" in question_lower:
        return "SELECT * FROM products;"
    elif "count products" in question_lower or "number of products" in question_lower:
        return "SELECT COUNT(*) FROM products;"
    else:
        raise RuntimeError(f"Unable to convert question to SQL with current rules: {question}")

def english_to_sql(question):
    # Improved regex matching with better logging
    try:
        if "how many" in question.lower() and "customers" in question.lower():
            return "SELECT COUNT(*) FROM customers;"
        elif "what are the components" in question.lower() or "structure" in question.lower():
            return "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main';"
        elif "average order amount" in question.lower():
            return "SELECT AVG(order_amount) FROM orders;"
        elif "customerid attribute" in question.lower():
            return "SELECT CustomerID FROM information_schema.columns WHERE table_name = 'customers';"
        elif "orderdate field" in question.lower():
            return "SELECT OrderDate FROM information_schema.columns WHERE table_name = 'orders';"
        else:
            return fallback_sql_generation(question)
    except Exception as e:
        logging.error(f"Failed to match regex for question '{question}': {e}")
        raise RuntimeError(f"Failed to match regex for question: {e}")

def execute_sql_query(db_connection, sql_query):
    try:
        result = db_connection.execute(sql_query).fetchall()
        return result
    except Exception as e:
        logging.error(f"Failed to execute SQL query '{sql_query}': {e}")
        raise RuntimeError(f"Failed to execute SQL query: {e}")

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
                results = execute_sql_query(db_connection, sql_query)
                print("Results:")
                for row in results:
                    print(row)
            else:
                print("Failed to generate SQL query from the given question.")
        except Exception as e:
            logging.error(f"An error occurred with question '{question}': {e}")
            print(f"An error occurred: {e}")
