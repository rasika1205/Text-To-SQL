![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Build Passing](https://img.shields.io/badge/build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-proprietary-lightgrey.svg)

---

# Text-To-SQL

A web application that translates natural language questions into SQL queries using a Large Language Model (LLM) and executes them on a MySQL database. Built with Flask, LangChain, and Gemini LLM.

## Features

- Converts natural language questions into accurate SQL queries using Gemini LLM via LangChain.
- Executes generated SQL queries on a configured MySQL database.
- Displays results in a user-friendly HTML format (table, text, or message).
- Handles empty results and error cases gracefully.
- Simple web interface for question submission.
- Secure handling of sensitive API keys and database credentials via environment variables.

## Demo
<img width="1682" height="872" alt="Screenshot 2025-07-14 183845" src="https://github.com/user-attachments/assets/c0f0092f-db0c-4d62-a10d-3ce3645e031f" />

## Technologies Used

- Python
- Flask
- LangChain
- Google Gemini (LLM via Google AI Studio)
- MySQL (via SQLAlchemy + PyMySQL)
- HTML, CSS

## Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/rasika1205/Text-To-SQL.git
   cd Text-To-SQL
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**  
   Create a `.env` file with the following keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   ```

4. **Run the app:**
   ```
   python app.py
   ```

5. **Visit:**
   Open [http://localhost:5000](http://localhost:5000) in your browser.

## Directory Structure

- `app.py` - Main application logic
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates (e.g., `index.html`, `result.html`)
- `static/` - CSS and static files

## Usage

- Enter your database question in natural language in the web form.
- The backend will:
  - Generate a SQL query using Gemini LLM.
  - Execute the query against your MySQL database.
  - Display results or error messages.
Here’s a suggested "Future Enhancements" section for your Text-To-SQL project’s README:

---

## Future Enhancements

- **Support for More Databases:** Extend compatibility to additional SQL dialects and database systems (e.g., PostgreSQL, MySQL, Oracle).
- **Natural Language Understanding Improvements:** Enhance the NLP models to better interpret complex queries, including nested questions and ambiguous statements.
- **User Authentication & Authorization:** Add user management features to ensure secure access and personalized query history.
- **Interactive Query Builder:** Integrate a visual interface to help users construct and validate their queries before execution.
- **Result Visualization:** Provide graphical representations of query results, such as charts and graphs, for improved data analysis.
- **Error Handling & Feedback:** Implement more informative error messages and suggestions to guide users in refining their queries.
- **API Integration:** Offer RESTful APIs for external applications to interact with the Text-To-SQL engine programmatically.
- **Multilingual Support:** Enable the system to process queries in multiple languages, broadening user accessibility.
- **Performance Optimization:** Improve response times and scalability, especially for large datasets and concurrent users.
- **Extensive Testing & Documentation:** Expand existing tests and enrich documentation to facilitate contributions and deployments.

---

## Notes

- Ensure your database user is read-only for safety.
- The application relies on correct environment variable configuration.

---

## License

This project is **proprietary** and protected by copyright © 2025 Rasika Gautam.

You are welcome to view the code for educational or evaluation purposes (e.g., portfolio review by recruiters).  
However, you may **not copy, modify, redistribute, or claim this project as your own** under any circumstances — including in interviews or job applications — without written permission.

---

Feel free to explore the code.

_Developed with 💡 by [Rasika Gautam](https://github.com/rasika1205)_
