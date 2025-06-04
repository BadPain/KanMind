# KanMind 🧠

**KanMind** is a web-based task and project management tool designed to help users visually organize their workflows. Users can create boards, split tasks into lists and cards, and enhance them with details such as descriptions, assignments, and deadlines.

---

## 🚀 Features

- 📝 User registration and login  
- 🗂️ Visual Kanban-style boards  
- 🛠️ Django Admin panel for managing data  
- 🔐 Secure authentication

---

## 🧰 Tech Stack

- [Django](https://www.djangoproject.com/) (Python)
- SQLite (Default local database)
- HTML/CSS (for frontend rendering)
- Django REST Framework *(optional, if added)*

---

## ⚙️ Local Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/BadPain/kanmind.git
   cd kanmind
   ```

2. **(Optional) Create and activate a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**  
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**  
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**  
   ```bash
   python manage.py runserver
   ```

7. Visit the app in your browser:  
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔐 Demo Credentials

You can use the following test user to explore the application:

```json
{
  "email": "florian123@example.com",
  "password": "password123"
}
```

Use the token for accessing protected API endpoints (e.g., include it as a `Authorization: Token <token>` header in Postman or your frontend).

---

## 🛡️ Admin Panel

You can access the Django admin panel at:  
[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---