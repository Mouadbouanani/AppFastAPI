#-------etape 1 : build des dependances ----
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

#----- etape 2 : image finale--------

FROM python:3.12-slim
WORKDIR /app

# Utilisateur non-root 

RUN useradd --create-home appuser

COPY --from=builder /install /usr/local
COPY main.py .

USER appuser
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000"]

