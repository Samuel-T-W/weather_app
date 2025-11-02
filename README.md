Weather App

A web app made by django that displays the weather of any given city.
The live version can be found here:
https://glacial-refuge-96892.herokuapp.com/

## Local Development Setup

Follow these steps to run the project on your local machine.

### 1. Prerequisites
* Python 3.9+
* [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### 2. Clone & Setup
```bash
# Clone the repository (if you haven't already)
# git clone https://github.com/your-username/weather_app.git
cd weather_app

# Install dependencies using Poetry
poetry install
```

### 3. Environment Variables
You will need an API key from OpenWeatherMap.

Create a `.env` file in the project root and add:
```
openweather_api_key="YOUR_API_KEY_HERE"
DEBUG=True  # Set to False in production
```

### 4. Database & Server
```bash
# Apply database migrations
poetry run python manage.py migrate

# Run the development server
poetry run python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Project Structure
* `weather/` - Weather app logic and views
* `users/` - User authentication and dashboard
* `weatherapp/` - Main Django project settings

## Deployment

### Heroku Deployment
For Heroku deployment, you'll need to export the Poetry dependencies to requirements.txt:

```bash
# Export dependencies for Heroku
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

Then deploy as usual:
```bash
git add .
git commit -m "Update dependencies"
git push heroku master
```

The `Procfile` and `runtime.txt` are already configured for Heroku deployment.
