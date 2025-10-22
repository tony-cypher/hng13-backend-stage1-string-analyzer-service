# 🧠 String Analyzer API  
A modern **FastAPI-based REST API** that analyzes strings, stores them in a PostgreSQL database, and provides insights like palindrome detection, word count, and more.

---

## 🚀 Features

- 🧩 **Create & store strings** with SHA-256 hashed IDs  
- 🧮 **Automatic string analysis** (length, palindrome check, unique characters, etc.)  
- 🔍 **Retrieve strings** by value or list all strings  
- 🧹 **Delete strings** safely from the database  
- 🧠 **Natural language filtering** (e.g., “all single word palindromic strings”)  

- ✅ Clean architecture with routes, services, and error layers  

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| Framework | [FastAPI](https://fastapi.tiangolo.com) |
| ORM | [SQLModel](https://sqlmodel.tiangolo.com) |
| Database | PostgreSQL (hosted on Render) |
| Driver | asyncpg |
| Server | Uvicorn |
| Language | Python 3.11+ |

---

## 📦 Project Structure

```
src/
├── db/
│   ├── main.py          # Async database setup
│   └── models.py        # SQLModel table definitions
├── routes/
│   └── string_to_analyze.py
├── services/
│   └── string_to_analyze_service.py
├── errors/
│   ├── exceptions.py
│   └── handlers.py
├── config.py            # Environment and settings
└── main.py              # FastAPI app entry point
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/string-analyzer-api.git
cd string-analyzer-api
```

### 2️⃣ Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate        # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` File
In the root directory, create a `.env` file and add your **Render PostgreSQL** connection URL:
```bash
DATABASE_URL=postgresql://<username>:<password>@<host>:5432/<database_name>
```

### 5️⃣ Run Database Migrations
The app automatically creates tables on startup using `SQLModel.metadata.create_all`.

### 6️⃣ Run the Application (Development)
```bash
uvicorn src.main:app --reload
```

App will be available at:
```
http://127.0.0.1:8000
```
Swagger Docs:
```
http://127.0.0.1:8000/docs
```

---

## 🧪 Example API Usage

### ➕ Create String
```bash
POST /strings
{
  "value": "racecar"
}
```

### 🔍 Get String
```bash
GET /strings/racecar
```

### 🗑️ Delete String
```bash
DELETE /strings/racecar
```

---

## 👨‍💻 Author

**Cipher Tony**  
💼 Backend Developer  

---

## 🪪 License

MIT License © 2025 Cipher Tony  
