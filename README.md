# User Registration & Login System

A Flask-based user authentication system with Neon PostgreSQL database, deployed on Render.

## Features
- User registration with validation (username: 4–25 chars, password: min 6 chars)
- User login with session management
- Password hashing with bcrypt
- User dashboard with profile management
- Email update functionality
- User listing feature (requires login)
- Account deletion
- Session-based authentication
- Neon PostgreSQL database integration
- Form validation with Flask-WTF
- Email validation
- Deployment on Render

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Madhav2005-Garg/GLA-B2-FLASK-CLASSWORK.git
   cd GLA-B2-FLASK-CLASSWORK
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```
   Edit `.env` with your database credentials:
   ```
   SECRET_KEY=<your-secret-key>
   DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>
   FLASK_ENV=development
   ```

5. **Run the application**
   ```bash
   python app/app.py
   ```
   > Database tables are created automatically on first run via `db.create_all()`.

6. **Access the application**
   - Home: http://localhost:5000/
   - Register: http://localhost:5000/register
   - Login: http://localhost:5000/login
   - Dashboard: http://localhost:5000/dashboard (after login)

## Project Structure
```
B2_Fullstack/
├── app/
│   ├── model/
│   │   └── users.py       # User model and database
│   ├── static/
│   │   └── favicon.ico    # Static files
│   ├── templates/
│   │   ├── base.html      # Base template
│   │   ├── dashboard.html # User dashboard
│   │   ├── login.html     # Login page
│   │   └── register.html  # Registration page
│   ├── app.py            # Main Flask application
│   └── form.py           # WTForms definitions
├── .env                  # Environment variables (not in repo)
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── render.yaml           # Render deployment config
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Technologies Used

- **Backend**: Flask 3.1.3 (Python web framework)
- **Database**: Neon PostgreSQL (serverless PostgreSQL) via psycopg2-binary
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Authentication**: bcrypt 5.0.0 for password hashing
- **Forms**: Flask-WTF 1.2.2 with WTForms 3.2.1 validation
- **Email Validation**: email-validator 2.0.0
- **Deployment**: Render (gunicorn 21.2.0)
- **Environment**: python-dotenv 1.2.2 for configuration

## User Model

| Field           | Type    | Description                  |
|-----------------|---------|------------------------------|
| `id`            | Integer | Primary key                  |
| `username`      | String  | Unique, max 80 chars         |
| `email`         | String  | Unique, max 120 chars        |
| `password_hash` | String  | bcrypt hashed password       |
| `created_at`    | DateTime| Account creation timestamp   |

## Available Routes
- `/` - Home page (redirects to dashboard if logged in, otherwise to register)
- `/register` - User registration
- `/login` - User login
- `/dashboard` - User dashboard (requires login)
- `/update-email` - Update user email (POST, requires login)
- `/fetch-users` - View all users (requires login)
- `/delete-account` - Delete user account (POST, requires login)
- `/logout` - User logout

## Deployment

### Render Deployment (Current)
The application is deployed on Render using `render.yaml` with:
- **Service name**: `b2-bharti-flask`
- **Database name**: `b2-bharti-db`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app.app:app`
- **Environment Variables**:
  - `SECRET_KEY`: Strong secret key for sessions
  - `DATABASE_URL`: Auto-linked from Render PostgreSQL database
  - `FLASK_ENV`: `production`

### Local Development
For local development:
1. Set up Neon database and get connection string
2. Configure `.env` file with your credentials (`FLASK_ENV=development`)
3. Run `python app/app.py`

> **Note**: The app runs with `debug=False` in all environments. To enable debug mode locally, set `debug=True` directly in `app.run()`.

### Manual Deployment
For other platforms:
1. Set environment variables (`FLASK_ENV=production`)
2. Use a production WSGI server (gunicorn)
3. Configure proper database credentials
4. Set a strong `SECRET_KEY`

## License
MIT
