# Forecast Testing Tool

This project automates the testing of forecasting models by sending test requests, adjusting model parameters, saving results in Excel/JSON formats, and backing up the database state.
---

## 📁 Project Structure

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

1. **Clone the repository** and navigate into the project directory:
```bash

   git clone https://github.com/VladimirKomov/model_testing_arima.git
   cd model_testing_arima/tester
```

2. **Install dependencies** using Poetry:
```bash

poetry install
```

3. **Activate the virtual environment** created by Poetry:
```bash

poetry shell
```

Configure database and other settings inside `.env` (just rename .env.exaple and add your data)file.


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


## Important Notes

- Test results are saved under `/forecast_test_results.<date>/`
- Database backups are saved under `/forecast_test_backups.<date>/`
- Backing up large tables (millions of rows) may take a significant amount of time.
- After each test, model parameters are automatically restored to their original state.
- Forecasting errors are logged but do not interrupt the testing sequence.
- The application is intended primarily for internal/company network use.

---

If you encounter any issues, check the logs inside the `/logs/` directory.

Happy Testing! 🚀

## 🔗 Author

- Vladimir Komov — [LinkedIn Profile](https://www.linkedin.com/in/vladkomov/)
- Feel free to connect with me on LinkedIn!