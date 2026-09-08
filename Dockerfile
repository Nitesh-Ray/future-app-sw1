# Dockerfile
# Builds a lightweight Python image with our FastAPI app.

# Use official Python 3.12 slim image
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv


# Set working directory inside the container
WORKDIR /app

# # Copy requirements first (better layer caching)
# COPY requirements.txt .

# Copy only dependency files first for caching
COPY pyproject.toml uv.lock* ./

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies using uv
RUN uv sync --frozen --no-dev --no-install-project

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy the rest of the application
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# # Command to run the server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Run the server
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]