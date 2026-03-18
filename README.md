# B2 Fullstack User Management

Minimal Flask application that demonstrates a full registration/login flow backed by PostgreSQL. It uses WTForms for validation, SQLAlchemy for data access, bcrypt for password hashing, and ships with production-ready config via `wsgi.py` + `render.yaml` for Render deployments.

## Key Features
- Registration with server-side validation (username length, unique username/email, password confirmation)
- Session-based login/logout with hashed credentials stored in PostgreSQL
- Authenticated dashboard that lets users update their email, list all users, or delete their account
- Responsive templates (`base`, `register`, `login`, `dashboard`) with a cohesive dark UI
- Automatic table creation on boot (`db.create_all()` inside the app context)
- Environment-aware database URI handling that upgrades `postgres://` strings to `postgresql+psycopg://`

## Tech Stack
| Layer | Technology |
| --- | --- |
| Web framework | Flask 3.1.3 |
| ORM | Flask-SQLAlchemy 3.1.1 |
| Forms & CSRF | Flask-WTF 1.2.2 + WTForms 3.2.1 |
| Auth | bcrypt 5.0.0 |
| Config | python-dotenv 1.2.2 |
| DB driver | `psycopg[binary]` |
| WSGI | gunicorn 23.0.0 (via `wsgi.py`) |

## Directory Layout
```
.
├── app/
│   ├── __init__.py            # Package marker
│   ├── app.py                 # Flask application & routes
│   ├── form.py                # WTForms form definitions
│   ├── model/
│   │   ├── __init__.py        # Package marker
│   │   └── users.py           # SQLAlchemy model + bcrypt helpers
│   ├── static/
│   │   └── favicon.ico        # Shared favicon
│   └── templates/
│       ├── base.html          # Shared layout/styles
│       ├── dashboard.html     # Authenticated dashboard
│       ├── login.html         # Login form
│       └── register.html      # Registration form
├── wsgi.py                    # gunicorn entry point (imports `app`)
├── requirements.txt           # Locked dependency versions
├── render.yaml                # Render service + database definition
├── .env.example               # Sample environment configuration
└── README.md
```

## Getting Started
1. **Clone & enter the repo**
	```bash
	git clone <your-fork-url>
	cd B2_Fullstack
	```
2. **Create a virtual environment**
	```bash
	python -m venv .venv
	.venv\Scripts\activate          # Windows
	source .venv/bin/activate        # macOS/Linux
	```
3. **Install dependencies**
	```bash
	pip install --upgrade pip
	pip install -r requirements.txt
	```
4. **Configure environment**
	```bash
	copy .env.example .env           # Windows
	cp .env.example .env             # macOS/Linux
	```
	Update `.env` with a real secret key and a PostgreSQL connection string. The application automatically transforms `postgres://` and `postgresql://` URLs into the SQLAlchemy-friendly `postgresql+psycopg://` format.
5. **Provision a PostgreSQL database** (Render, Neon, Supabase, etc.) and drop the connection string into `DATABASE_URL`.
6. **Run the server**
	```bash
	python app/app.py
	```
	The app loads variables via `python-dotenv`, initializes SQLAlchemy, and calls `db.create_all()` on startup so no extra migration step is required for the first run.

> **Debug note:** `app.run(debug=os.getenv("FLASK_ENV") == "production")` mirrors the existing code. Set `FLASK_ENV=production` to enable debug mode locally, or edit the last line of `app/app.py` for the behavior you prefer.

## Environment Variables
| Name | Required | Description |
| --- | --- | --- |
| `SECRET_KEY` | Yes | Flask session/signing key. Use a long random string in production. |
| `DATABASE_URL` | Yes | PostgreSQL connection string (e.g. `postgresql://user:pass@host:5432/db`). automatically upgraded to `postgresql+psycopg://`. |
| `FLASK_ENV` | Optional | Controls the debug toggle logic above and is exported to the templates. Defaults to `production` in `.env.example`. |

## Database Model
`app/model/users.py` defines a single `Users` table with:
- `id`, `username`, `email`, `password_hash`, `created_at`
- `set_password()` / `check_password()` helpers that wrap bcrypt hashing & verification

Because `db.create_all()` executes inside the application context, tables are created the first time the process starts (no Alembic/AUTO migrations included).

## Routes
- `/` – redirect helper (sends authenticated users to `/dashboard`, guests to `/register`)
- `/register` – GET/POST registration with duplicate username/email checks
- `/login` – GET/POST login that stores `user_id` + `username` in the session
- `/dashboard` – Auth-only dashboard rendering the username, email, optional flash message, and optional user list
- `/update-email` – POST endpoint to update the logged-in user email with uniqueness enforcement
- `/fetch-users` – GET endpoint that loads all users and re-renders the dashboard with the table
- `/delete-account` – POST endpoint that deletes the current user, clears the session, and redirects to login
- `/logout` – GET endpoint that clears the session and redirects to login

Each mutating route guards against missing sessions and rolls back the DB session on failure.

## Frontend
- `base.html` contains the shared typography, theming, and layout primitives used by login/register.
- `dashboard.html` implements cards for email update, listing all users, and a dangerous delete-account block plus responsive table styles.
- Forms render WTForms labels/fields and loop across validation errors.

## Deployment (Render)
`render.yaml` provisions:
- A managed PostgreSQL instance named `b2-bharti-db` whose connection string is automatically exposed to the service.
- A web service named `b2-bharti-flask` that runs `pip install -r requirements.txt` during build and starts with `gunicorn wsgi:app`.
- `SECRET_KEY` is marked as `sync: false` so you set it via the Render dashboard, while `FLASK_ENV` defaults to `production`.

For other providers, reuse the same `gunicorn wsgi:app` command and replicate the three environment variables above.

## License
MIT
