# Simple FastAPI CRUD API

Minimal REST API using FastAPI, SQLAlchemy, and SQLite.

## Setup

commit this repo

cd repo

1. Create a virtual environment (optional but recommended):
```bash
    uv init
    uv venv
    uv add fastapi uvicorn[standard] sqlalchemy pydantic
    ```
or

```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   uvicorn main:app --reload

## testing
```bash
    uv add pytest httpx
```

run  `pytest`


## Docker

You can run the application in Docker for easy setup and deployment.

1. Make sure Docker and Docker Compose are installed.

2. Build and start the container:
   ```bash
   docker-compose up --build

Open `http://localhost:8000/` or
`http://127.0.0.1:8000/` in your browser.

To stop the container:

```bash
    docker-compose down
```

## Continuous Integration

This project uses GitHub Actions to run tests automatically on every push and pull request.  
The workflow is defined in `.github/workflows/ci.yml`.

You can add a status badge to your README (replace `USERNAME` and `REPO`):
```markdown
![CI](https://github.com/USERNAME/REPO/actions/workflows/ci.yml/badge.svg)


---

## How to Use

1. **Create the `.github/workflows` folder** in your project root.
2. **Add the `ci.yml` file** with the content above.
3. **Commit and push to GitHub.**  
   The workflow will run automatically.

You can watch the progress in the **Actions** tab of your repository.

---

## What This Demonstrates

- **Automated testing** – every code change is verified.
- **CI/CD basics** – using GitHub Actions, the most popular CI service.
- **Project health** – gives confidence when adding new features.

---

## Next Steps

Now your project is fully professional. You could continue with:

- **Deploy to a cloud platform** (Render, Railway, AWS, GCP) – use Docker and CI/CD.
- **Switch to PostgreSQL** – add a database service to `docker-compose.yml` and update the `DATABASE_URL`.
- **Add code coverage** – measure test coverage with `pytest-cov` and integrate it into CI.
- **Add linting** – use `ruff` or `black` to enforce code style.

Which of these would you like to explore next?



## Database

By default, the app uses SQLite (file `test.db`) for local development without Docker.  
When running with Docker Compose, it automatically uses PostgreSQL (see `docker-compose.yml`).

To use PostgreSQL locally without Docker, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL=postgresql://user:password@localhost:5432/mydb