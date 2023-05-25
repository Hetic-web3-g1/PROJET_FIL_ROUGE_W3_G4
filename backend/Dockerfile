# Development stage
FROM python:3.9 AS development

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirement.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy the entire project to the container
COPY . .

# Set environment variables
# ENV FASTAPI_ENV=development
# ENV PYTHONUNBUFFERED=1
ENV FRONTEND_PORT=3000

# Start the FastAPI app with auto-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]

# # ------------------------------------------------------------------------

# Production stage
FROM python:3.9 AS production

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirement.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy the entire project to the container
COPY . .

# Set environment variables
# ENV FASTAPI_ENV=development
# ENV PYTHONUNBUFFERED=1
ENV FRONTEND_PORT=3000

# Start the FastAPI app with no auto-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]