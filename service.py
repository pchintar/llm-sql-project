from validator import validate_and_execute
from llm import ask_llm
from schema import get_schema

def query(question, table):
    schema = get_schema(table)
    sql = ask_llm(question, table, schema)
    results, msg = validate_and_execute(sql)
    return results, sql, msg
