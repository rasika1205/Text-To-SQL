from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from flask import Flask, request, render_template, redirect, url_for, flash
import re,os

api_key=os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database_schema = os.getenv("DB_NAME")
MYSQL_URI = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"

db = SQLDatabase.from_uri(MYSQL_URI, sample_rows_in_table_info=2)

template = """
Based on the table schema below, write a SQL query that would answer the user's question:
Remember : Only provide me the sql query dont include anything else.
           Provide me sql query in a single line dont add line breaks.
Table Schema:
{schema}

Question: {question}
SQL Query:
"""

prompt  = ChatPromptTemplate.from_template(template)
llm     = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                                 api_key=api_key,
                                 temperature=0)
sql_chain = (
    RunnablePassthrough.assign(schema=lambda _: db.get_table_info())
    | prompt
    | llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

app.secret_key = "replace‑me"        # enables flash()

def extract_query(llm_text: str) -> str | None:
    """
    Pull the first plausible SELECT query out of the LLM response.
    Falls back to ```sql ``` fences if present.
    """

    m = re.search(r"\bSELECT\b[\s\S]*?(?:;|$)", llm_text, re.IGNORECASE)
    if not m:
        return None
    q = m.group(0).strip()
    if not q.endswith(";"):
        q += ";"
    return q
# … imports, config, db, sql_chain, extract_query() stay the same …
import ast
from collections.abc import Mapping

def classify_sql_result(raw):
    """
    Returns:
      ("table", list[dict])   – ready for HTML table
      ("text",  str)          – scalar value or message
      ("empty", None)         – no rows
    """
    if raw in (None, [], ''):
        return "empty", None

    # If LangChain's db.run() returned a str representation, e.g. "[(1356976.996,)]"
    if isinstance(raw, str):
        try:
            parsed = ast.literal_eval(raw)
            # parsed is now list|tuple|scalar
        except Exception:
            return "text", raw.strip()
    else:
        parsed = raw

    # 1‑row scalar?  e.g. [(1356976.996,)]
    if isinstance(parsed, (list, tuple)) and parsed and isinstance(parsed[0], (list, tuple)):
        # wrap into a list‑of‑dict with a generic column name
        return "table", [{"value": row[0] if len(row)==1 else tuple(row)} for row in parsed]

    # list[dict] already? keep
    if isinstance(parsed, list) and isinstance(parsed[0], Mapping):
        return "table", parsed

    # anything else → str
    return "text", str(raw).strip()


@app.get("/")                                   # 1️⃣  Just the form
def index():
    """Display the question form."""
    return render_template("index.html")        # no flash logic needed here


@app.post("/ask")                               # 2️⃣  Handle submission
def ask():
    """Process a question, run the SQL, show the result template."""
    question = request.form.get("question", "").strip()
    if not question:
        flash("Please enter a question 😊", "warning")
        return redirect(url_for("index"))

    # 1. LLM → SQL
    try:
        llm_resp = sql_chain.invoke({"question": question})
    except Exception as e:
        flash(f"LLM error: {e}", "danger")
        return redirect(url_for("index"))

    sql_query = extract_query(llm_resp)
    if not sql_query:
        flash("LLM did not return a SQL query 🤷‍♂️", "danger")
        return redirect(url_for("index"))

    # 2. Execute SQL (read‑only user strongly advised)
    try:
        result = db.run(sql_query)              # list[dict]
    except Exception as e:
        return render_template(
            "result.html",
            question=question,
            sql_query=sql_query,
            kind="text",
            result=f"MySQL error → {e}",
        )
    kind, result = classify_sql_result(result)
    # 3. Render the dedicated *result* page
    return render_template(
        "result.html",
        question=question,
        sql_query=sql_query,
        result=result,
        kind=kind
    )



if __name__ == "__main__":
    app.run(debug=True)