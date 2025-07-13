#!/usr/bin/env bash

if [ "$ENV" = "local" ] || [ "$ENV" = "dev" ]; then
  echo "Waiting for the database initialization... "
  sleep 5;
fi

echo "Running migrations... "
# Try to run migrations, but continue even if it fails
python manage.py migrate || {
  echo "Warning: Migration failed, but continuing anyway..."
  # Check if database tables exist by trying to count CV objects
  python manage.py shell -c "from apps.main.models import CV; print(CV.objects.count())" > /dev/null 2>&1 || {
    echo "Error: Database tables don't exist or are not accessible. Exiting."
    exit 1
  }
}

# Create a flag file to track if fixtures have been loaded
FLAG_FILE="/tmp/fixtures_loaded"

# Check if fixtures have been loaded in this container
if [ ! -f "$FLAG_FILE" ]; then
  echo "Loading fixtures (first run)... "
  # Use --ignorenonexistent to skip records that already exist
  python manage.py loaddata fixtures/cv_data.json --ignorenonexistent
  
  # Create flag file to prevent reloading
  touch "$FLAG_FILE"
  
  echo "Fixtures loaded successfully."
else
  echo "Fixtures already loaded in this container. Skipping."
fi

echo "Collecting static files... "
rm -rf staticfiles
python manage.py collectstatic --noinput

echo "Starting project... "
if [ "$ENV" = "local" ]; then
  python manage.py runserver 0.0.0.0:8000
elif [ "$ENV" = "dev" ]; then
  python manage.py runserver 0.0.0.0:8000
else
  gunicorn CVProject.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120
fi 