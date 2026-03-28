# 📝 TodoList - Task Management Web App

A lightweight and user-friendly To-Do List web application that helps users manage daily tasks efficiently with a clean and intuitive interface.

---

## 📌 Features

* ✅ Add new tasks
* ✏️ Edit existing tasks
* ✔️ Mark tasks as completed
* ❌ Delete tasks
* 📱 Responsive and clean UI
* ⚡ Fast and simple performance

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, Bootstrap
* **Database:** SQLite

---

## 📂 Project Structure

todo-app/
│
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes.py            # All routes (URL handling)
│   ├── models.py            # Database models
│   ├── forms.py             # Forms (optional - WTForms)
│   │
│   ├── templates/           # HTML files (Jinja2)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── add_task.html
│   │   ├── update_task.html
│   │
│   ├── static/              # CSS, JS, Images
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── images/
│   │
│   └── database.db          # SQLite database
│
├── migrations/              # (Optional) for Flask-Migrate
│
├── config.py                # App configuration
├── run.py                   # Entry point to run app
├── requirements.txt         # Dependencies
├── README.md                # Project description
└── .env                     # Environment variables
---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/rr9299250/TodoList.git
```

### 2️⃣ Navigate to Project Folder

```bash
cd TodoList
```

### 3️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
```

Activate it:

* Windows:

```bash
venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application

```bash
python app.py
```

---

## 🌐 Usage

1. Open your browser
2. Go to: `http://127.0.0.1:5000/`
3. Start adding your daily tasks
4. Mark tasks as complete or delete them easily

---

## 📸 Screenshots

*(Add screenshots here to make your project more attractive)*


## 👨‍💻 Author

**Rohit Raj**

* GitHub: https://github.com/rr9299250

---

## ⭐ Support

If you like this project, please ⭐ star the repository and share it!
