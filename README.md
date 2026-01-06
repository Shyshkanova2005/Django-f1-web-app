# Formula 1 Fan Web App (Django)
A Django-based fan web application dedicated to Formula 1 2025 season providing detailed information about
drivers, teams, race calendar, statistics, standings and detailed pages.
The project is built as a full-stack web application using Django, PostgreSQL, and Bootstrap, with dynamic content stored in a database.

# Features
Formula 1 drivers & teams pages with detailed profiles
Race calendar with status (completed / next / upcoming)
Statistics of championship progress, fastest laps, pole positions, podiums and dnfs (didn't finish)
Driver & Team standings
Images and data stored in database (fixtures)
Authentication (login / logout)

# Tech Stack
Backend: Django (Python)
Database: PostgreSQL
Frontend: HTML, CSS, Bootstrap, JavaScript
Media & Static: Django static and media files

## Screenshots

## Home Page
<img src="docs/screenshots/main_first_page.png" width="70%" />
<img src="docs/screenshots/main_second_page.png" width="70%" />

## Teams Page
<img src="docs/screenshots/teams.png" width="70%" />

## Team Details (Different Team Styles)
<p align="center">
  <img src="docs/screenshots/teams_mclaren.png" width="45%" />
  <img src="docs/screenshots/teams_williams.png" width="45%" />
</p>

## Driver Details (Different Driver Cards)
<p align="center">
  <img src="docs/screenshots/driver.png" width="45%" />
  <img src="docs/screenshots/drivers.png" width="45%" />
</p>

## Tracks
<img src="docs/screenshots/tracks.png" width="70%" />

## Statistics
<img src="docs/screenshots/statistics_first_part.png" width="70%" />
<img src="docs/screenshots/statistics_second_part.png" width="70%" />

## Authorization
<img src="docs/screenshots/authorize.png" width="70%" />

## User Profile
<img src="docs/screenshots/profile.png" width="70%" />

# Database & Fixtures
The project includes pre-filled database data stored as Django fixtures.
All main content (teams, drivers, statistics, images paths, slugs, texts, etc.) is located in:
```
fixtures/data_site.json
```
This allows the project to be fully restored with the same data after cloning the repository.

# Load data into the database
After applying migrations, load the data using:
```
python manage.py loaddata fixtures/data_site.json
```
(Images are stored locally in static/ and media/ directories and are referenced via database fields.)

# How to Run Locally
## Clone the repository
```
git clone https://github.com/Shyshkanova2005/Django-f1-web-app.git
cd Django-f1-web-app
```

## Install dependencies
```
pip install -r requirements.txt
```

## Configure environment variables
Create a .env file (or set environment variables manually) and add:
```
SECRET_KEY=your-secret-key
```
The SECRET_KEY is not included in the repository for security reasons.

## Apply migrations
```
python manage.py migrate
```

## Load fixtures (database data)
```
python manage.py loaddata fixtures/data_site.json
```

## Run the development server
```
python manage.py runserver
```
