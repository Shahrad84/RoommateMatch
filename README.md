# RoommateMatch

A Django-based roommate matching application with AI-powered compatibility analysis.

## Features

* User authentication (register, login, logout)
* Multi-step profile completion form
* Dashboard with feature unlocking
* Account overview page
* AI-powered matching via OpenRouter
* Hard filters for compatibility requirements:

  * Pets
  * Smoking
  * Noise
  * Sleep schedule
* Same-city user matching

## Tech Stack

* **Django 6.0**
* **PostgreSQL**
* **OpenRouter API**
* **HTML / CSS / JavaScript**

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## AI Setup

1. Go to [OpenRouter](https://openrouter.ai/) and create an account.
2. Generate an API key.
3. Add your API key to `matching/views.py`:

```python
API_KEY = "your-key"
```

> For production, it is recommended to store the API key in an environment variable instead of directly in the source code.

## Create Test Users

You can generate test users with randomized profiles, lifestyles, and preferences:

```bash
python manage.py create_test_users
```

This command creates **30 test users in Berlin**.

## Key URLs

| URL                   | Description              |
| --------------------- | ------------------------ |
| `/dashboard/`         | Dashboard                |
| `/profile/complete/`  | Complete profile         |
| `/match/explore/`     | Explore roommate matches |
| `/accounts/overview/` | Account overview         |

## Project Structure

```text
RoommateMatch/
├── accounts/              # User authentication
├── profiles/              # Profile, Lifestyle, and Preference models
├── matching/              # Matching system and AI analysis
├── locations/             # City and Country models
├── frontend-section/      # Templates and static files
└── manage.py
```

## Matching Algorithm

The matching process consists of the following steps:

### 1. Candidate Selection

The system randomly selects up to **20 users from the same city** as potential roommates.

### 2. Hard Filters

Users who violate important compatibility requirements are rejected before AI analysis.

Examples include:

* Pet preferences
* Smoking preferences
* Noise tolerance
* Sleep schedules

### 3. AI Compatibility Analysis

Users who pass the hard filters are sent to an AI model through the **OpenRouter API** for deeper compatibility analysis.

The AI evaluates the users' profiles and generates:

* Compatibility score
* Positive compatibility points
* Potential concerns

### 4. Results

The compatibility results are presented to the user so they can explore potential roommate matches.

## Current Status

### Completed

* [x] User authentication
* [x] Profile completion with a 3-step form
* [x] Hard filters for matching
* [x] AI compatibility analysis via OpenRouter
* [x] Dashboard with feature unlocking
* [x] Account overview

### To Do

* [ ] Like / Skip system with database storage
* [ ] Matches page
* [ ] Messaging between matched users
* [ ] User profile photos
* [ ] WebSocket-based real-time matching
* [ ] Celery-based background AI processing

## License

This project is licensed under the MIT License.

