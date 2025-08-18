## Music Streaming Service (Django)

[![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A simple music streaming web application built with Django. It lets users browse albums and tracks, play music, manage playlists, and update their profiles. Admins can add and manage music, albums, and users.

### Features

- **User accounts**: Register, log in, profile with image upload
- **Music browsing**: View albums and tracks, built-in audio player
- **Playlists**: Create playlists and add tracks
- **Admin console**: Manage music, albums, and users
- **Media handling**: Sample music and images included under `media/`

### Tech Stack

- **Backend**: Django 5
- **Database**: PostgreSQL
- **Libraries**: Pillow (images), pyotp, django-environ
- **Python**: 3.10+ recommended

---

### Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Git

---

### Quick Start (Windows PowerShell)

1. Clone and enter the project directory

```powershell
git clone https://github.com/harshavardana-reddy/Music_Streaming_Services_Django.git
cd mss
```

2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies

```powershell
pip install -r requirements.txt
```

4. Configure PostgreSQL

- Create a database named `mss_db`
- Ensure a user with access (defaults in `mss/settings.py` are `postgres` / `root` on `localhost:5432`)
- Either update your local DB to match these values or edit `mss/settings.py` to reflect your environment

5. Apply database migrations

```powershell
python manage.py migrate
```

6. Create an admin user

```powershell
python manage.py createsuperuser
```

7. Run the server

```powershell
python manage.py runserver
```

8. Open in your browser

- Site: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

---

### Important URLs

- **Home**: `/`
- **Auth**: `/login/`, `/register/`
- **User area (prefixed)**: `/user/`
  - `/user/userhome/` – user dashboard
  - `/user/viewalbums/`, `/user/viewmusic/`
  - `/user/createplaylist/`, `/user/viewplaylists/`
  - `/user/musicplayer/`
  - `/user/profile/`, `/user/update_profile`, `/user/update_profile_image`
  - `/user/logout/`
- **Admin area (Django)**: `/admin/`
- **Admin area (custom, prefixed)**: `/admincfg/`
  - `/admincfg/adminhome/`
  - `/admincfg/addmusic/`, `/admincfg/addalbum/`
  - `/admincfg/viewmusic/`, `/admincfg/viewalbum/`, `/admincfg/viewusers/`
  - `/admincfg/musicplayer/`

---

### Media and Static

- `MEDIA_URL` is `/media/` and is served automatically when `DEBUG=True`
- `MEDIA_ROOT` points to the local `media/` folder
- Sample music and images are included under `media/` to help you get started

---

### Configuration and Secrets

- Default settings (DB credentials, `SECRET_KEY`, email) are currently in `mss/settings.py` for development convenience. Change them before deploying.
- Email is configured for Gmail SMTP. For local development you can switch to the console email backend by setting:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

- If you prefer environment variables, integrate `django-environ` in `mss/settings.py` and load values from a `.env` file. Remember to keep `.env` out of version control.

---

### Troubleshooting

- If `psycopg2` fails to install on Windows, ensure PostgreSQL is installed and its development libraries are available. Alternatively, try `psycopg2-binary` for local development.
- If media files do not display, confirm `DEBUG=True` and that you are accessing them via `/media/...` paths.

---

### Project Structure (key paths)

```
mss/
  manage.py
  mss/                # Project settings and root URLs
  user/               # User-facing app (views, urls, models)
  admincf/            # Admin/custom admin app (views, urls, models)
  templates/          # HTML templates
  media/              # Sample media (music and images)
  requirements.txt
  README.md
  LICENSE
```

---

### License

This project is released under the MIT License. See `LICENSE` for details.
