# CV Project

Django application for managing CVs with PDF export, email sending, and translation to different languages.

## Features

- **Full Docker automation** - everything is configured and ready to run
- CV export to PDF format
- Email CV sending via Celery
- CV translation to different languages using OpenAI API
- Request audit system
- Test coverage according to technical requirements
- PEP8 compliance
- Full code typing

## Quick Start

### 1. Clone the project
```bash
git clone <repository-url>
cd DTEAM-django-practical-test
```

### 2. Environment setup
Create a `.env` file in the project root based on `.env.example`:
```bash
cp .env.example .env
```

Edit the `.env` file, filling in the necessary values (especially `SECRET_KEY` and `OPENAI_API_KEY`).

### 3. Run the project
```bash
docker compose up -d
```

All necessary operations (migrations, dependency installation, database setup) are performed automatically when starting containers.

### 4. Access the application
The application will be available at: **http://127.0.0.1:8000**

## Testing

The project contains a complete test suite according to technical requirements.

Run tests:
```bash
docker compose exec django pytest -v
```

## Code Quality

### Linting and formatting (Ruff)
The project complies with PEP8 standards. Ruff is used as linter and formatter.

Run checks:
```bash
docker compose exec django ruff check .
```

### Type checking (MyPy)
The project is fully typed. Checking may take some time.

Run type checking:
```bash
docker compose exec django mypy .
```

## Email Testing

MailHog is used for email testing, available at:
**http://127.0.0.1:8025**

All sent emails can be viewed in the MailHog web interface.

## Architecture

The project consists of the following services:
- **Django** - main application (port 8000)
- **PostgreSQL** - database (port 5432)
- **Redis** - message broker for Celery (port 6379)
- **Celery** - background task processing
- **MailHog** - SMTP server for testing (port 8025)

## Main Features

- List of all CVs
- Detailed CV view
- CV export to PDF
- Send PDF via email
- CV translation to various languages
- Audit system for all HTTP requests
- Application settings

## Development

To connect to the Django container for development:
```bash
docker compose exec django bash
```

View logs for all services:
```bash
docker compose logs -f
```

## Commit Guidelines

Follow commit message [conventions](https://www.conventionalcommits.org/en/v1.0.0/) to maintain a clean and consistent commit history:

- **feat**: a new feature.
- **fix**: a bug fix.
- **chore**: a routine task, maintenance.
- **refactor**: a refactoring or for a code change that neither fixes a bug nor adds a feature.
- **perf**: a code change that improves performance.
- **test**: for adding or modifying tests.
- **build**: for changes that affect the build system or external dependencies.
- **ci**: for changes related to CI/CD and scripts.
- **docs**: for documentation changes.
- **style**: for code style changes. 