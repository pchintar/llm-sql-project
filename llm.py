import httpx
import re
import os

def ask_llm(question, table_name, schema):
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return "SELECT * FROM " + table_name + " LIMIT 5"
    
    schema_str = ', '.join([f"{col['name']} ({col['type']})" for col in schema])
    
    prompt = f"Table: {table_name} with columns: {schema_str}\nQuestion: {question}\nReturn ONLY the SQLite SELECT query, no markdown, no explanation."
    
    response = httpx.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}'},
        json={
            'model': 'llama-3.3-70b-versatile',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0
        },
        timeout=30
    )
    
    if response.status_code != 200:
        return "SELECT * FROM " + table_name + " LIMIT 5"
    
    sql = response.json()['choices'][0]['message']['content']
    sql = re.sub(r'```sql\n?|```\n?', '', sql)
    return sql.strip()
