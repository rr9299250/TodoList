# ✅ TaskFlow — Professional To-Do List App

A modern, dark-themed task management web app built with **Flask**, **SQLite**, and **Bootstrap 5**.

---

## 📁 Project Structure

```
todo_app/
├── app.py                    # Main Flask application & routes
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── instance/
│   └── taskflow.db           # SQLite database (auto-created)
├── templates/
│   ├── base.html             # Base layout (sidebar + topbar)
│   ├── index.html            # Dashboard (task list)
│   ├── add_task.html         # Add new task form
│   ├── update_task.html      # Edit task form
│   ├── 404.html              # Not Found error page
│   └── 500.html              # Server Error page
└── static/
    ├── css/
    │   └── style.css         # All custom styles
    └── js/
        └── app.js            # JavaScript (toggle, modal, search)
```

---

## 🚀 Setup & Run Locally

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Clone / Download the project
```bash
cd todo_app
```

### 3. Create a virtual environment (recommended)
```bash
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the app
```bash
python app.py
```

### 6. Open in browser
```
http://127.0.0.1:5000
```

The SQLite database (`taskflow.db`) is created automatically on first run.

---

## ✨ Features

| Feature                 | Details                                      |
|-------------------------|----------------------------------------------|
| **CRUD Operations**     | Create, Read, Update, Delete tasks           |
| **Task Priority**       | Low / Medium / High with color coding        |
| **Due Dates**           | Overdue tasks highlighted in red             |
| **Status Toggle**       | Instant AJAX toggle (no page reload)         |
| **Filter Tasks**        | All / Pending / Completed                    |
| **Search**              | Live debounced search by title               |
| **Flash Messages**      | Success/error notifications                  |
| **Responsive UI**       | Works on desktop, tablet, and mobile         |
| **Dark Theme**          | Elegant dark luxury aesthetic                |
| **Animations**          | Smooth card entrances, hover effects, toasts |

---

## 🔌 API Routes

| Method | Route                   | Description             |
|--------|-------------------------|-------------------------|
| GET    | `/`                     | Dashboard (task list)   |
| GET    | `/?status=Pending`      | Filter by status        |
| GET    | `/?search=keyword`      | Search tasks            |
| GET    | `/add`                  | Add task form           |
| POST   | `/add`                  | Submit new task         |
| GET    | `/update/<id>`          | Edit task form          |
| POST   | `/update/<id>`          | Submit task update      |
| POST   | `/delete/<id>`          | Delete a task           |
| POST   | `/toggle/<id>`          | Toggle task status (AJAX)|

---

## 🗄️ Database Schema

```sql
CREATE TABLE tasks (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  title       VARCHAR(200) NOT NULL,
  description TEXT,
  status      VARCHAR(20)  DEFAULT 'Pending',
  priority    VARCHAR(10)  DEFAULT 'Medium',
  due_date    DATE,
  created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask 3, Flask-SQLAlchemy
- **Database**: SQLite (via SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Vanilla JS
- **Icons**: Bootstrap Icons
- **Fonts**: Syne + DM Sans (Google Fonts)
- **Templating**: Jinja2
