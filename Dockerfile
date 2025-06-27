# Use Python 3.10.12 slim image
FROM python:3.10.12-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Copy application code
COPY . .

# Install dependencies
RUN poetry install --no-root

# Expose port (FastAPI default)
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]