FROM python:3.12.4-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Ensure clean_data is present at the correct path for the app
RUN mkdir -p src/clean_data && cp -r src/clean_data/* src/clean_data/
CMD ["uvicorn", "src.hr_analysis.api.main:app", "--host", "0.0.0.0", "--port", "10000"]