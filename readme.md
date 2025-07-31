# StreamQL

Simple FastAPI backend with a React frontend for managing projects and running SQL queries against imported CSV files.

## Backend

The backend requires Python 3.10+.

Install dependencies and run the API:

```bash
pip install -r requirements.txt
uvicorn logic.app:app --reload
```

The first run will create a `~/streamql` workspace containing databases and uploaded files.

## Frontend

The React frontend lives in the `ui` folder and uses Vite.

```bash
cd ui
npm install
npm run dev
```

This will start the development server on port 5173.
