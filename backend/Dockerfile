# Build context is the repository root (see docker-compose.yml) so the image can
# install the sibling dt_genai GenAI package alongside the backend.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Backend dependencies first (better layer caching).
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install the GenAI package so app/integrations/genai.py uses the real copilot
# instead of the deterministic fallback.
COPY genai /genai
RUN pip install --no-cache-dir /genai

# Backend source.
COPY backend .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
