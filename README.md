# Forecast Testing Tool

This project is designed to automate forecasting model testing by sending test requests, adjusting model parameters, saving results to Excel/JSON, and backing up the database state.

## Project Structure

```
tester/
 ├── app/
 │    ├── core/          # Configuration and logging
 │    ├── databases/     # Database connection
 │    ├── logs/          # Application logs
 │    ├── models/        # SQLAlchemy ORM models
 │    ├── queries/       # Raw SQL queries
 │    ├── routers/       # FastAPI routes
 │    ├── schemas/       # Pydantic schemas
 │    ├── services/      # Business logic
 │    └── utils/         # Helper modules (saving results, creating backups)
 ├── forecast_test_backups.YYYYMMDD/    # Daily backup folder (generated)
 ├── forecast_test_results.YYYYMMDD/    # Daily results folder (generated)
 ├── .env                               # Environment variables
 ├── poetry.lock
 ├── pyproject.toml
 └── .gitignore
```

## Installation

Clone the repository and navigate into the project:

```bash

cd tester
```

Install dependencies using Poetry:

```bash

poetry install
```

Configure database and other settings inside `.env` file.


## Running the Application

Start the FastAPI application with:

```bash

poetry run uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

- API will be available at: `http://localhost:8001`
- Swagger UI (interactive API docs): `http://localhost:8001/docs`


## Features

- Initial Forecast Run (`/run-initial-test`)
- Multiple Parameterized Test Runs (`/run-multi-test`)
- Automatic parameter backup and restoration
- Saving results as Excel + JSON
- Full database backup (`ds_data` table)
- Organized backup folders by date


## Notes

- Results are stored under `/forecast_test_results.<date>/`
- Backups are stored under `/forecast_test_backups.<date>/`
- Large tables (millions of rows) might take some time to backup.

## Notes_2
- Full ds_data backups may be slow for large tables (2M+ rows).
- Parameter values are always reverted to original after each test.
- Forecasting errors are logged but won't stop the test sequence.
- The service is designed primarily for internal/company network use.

---

If you encounter any issues, check the logs inside the `/logs/` directory.

Happy Testing! 🚀

