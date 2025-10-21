#  String Analysis API (FastAPI)

A simple yet powerful FastAPI service that allows users to store, analyze, and query strings based on properties like palindrome status, word count, and more.  
It also supports **natural language filtering** for intuitive data queries.

---

## Features

- Create and store analyzed strings  
- Filter strings by multiple query parameters  
- Filter using **natural language** (e.g., “strings longer than 5 characters that are palindromes”)  
- Automatic detection of string properties (length, palindrome, word count, etc.)  
- Proper error handling and validation

---

## Tech Stack

- **FastAPI** 
- **SQLAlchemy** 
- **Postgresql**
- **Pydantic**
- **Uvicorn** 

---

## Setup Instructions

### 1 Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```
---

## 2. Create and activate a virtual environment

python -m venv venv

venv\Scripts\activate    # for Windows
or
source venv/bin/activate # for Mac/Linux

---

## 3. Install dependencies
pip install -r requirements.txt

---

## 4. Set environment variables

Create a .env file in the project root and add:

DATABASE_HOSTNAME=YOUR_DB_HOSTNAME
DATABASE_PORT=YOUR_DB_PORT
DATABASE_PASSWORD=YOUR_DB_PASSWORD
DATABASE_NAME=YOUR_DB_NAME
DATABASE_USERNAME=YOUR_DB_USERNAME

---

## 5. Run the server
uvicorn app.main:app --reload

Visit: http://127.0.0.1:8000/

---

### API Endpoints

## Post/ - Create a new string

Request Body:

{
  "value": "racecar"
}

Success Response (201):

{
  "id": 1,
  "value": "racecar",
  "properties": {
    "is_palindrome": true,
    "length": 7,
    "word_count": 1
  },
  "created_at": "2025-10-20T19:00:00Z"
}

Error Responses:

- 400 Bad Request: Invalid body or missing "value" field

- 409 Conflict: String already exists

- 422 Unprocessable Entity: Invalid type for "value" (must be string)


GET / — List strings with filters

Query Parameters (optional):

- is_palindrome: bool

- min_length: int

- max_length: int

- word_count: int

- contains_character: str (single character)


Error Response:

400 Bad Request: Invalid query parameter values or types


GET /filter-by-natural-language — Filter strings via NL query


Example Request:

GET /filter-by-natural-language?query=strings longer than 5 characters


Error Responses:

- 400 Bad Request: Unable to parse natural language query

- 422 Unprocessable Entity: Invalid input type for query


Example Natural Language Queries

- “strings longer than 5 characters”   -   min_length = 6
- “palindrome strings only”  -	is_palindrome = true
- “strings containing the letter a”  -	contains_character = "a"

---

## 🪄 Author

Name: Haneef Ojuatalyo
Email: haneefojutalayo@gmail.com

Stack: Python/FastAPI
Track: HNG Backend
