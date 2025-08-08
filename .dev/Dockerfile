# Base Ubuntu
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

COPY . /app

RUN apt-get update && \
    apt-get install -y curl gnupg python3 python3-pip python3-venv build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN npm install -g @angular/cli

RUN pip3 install --no-cache-dir -r /app/backend/requirements.txt

WORKDIR /app

EXPOSE 8000

EXPOSE 4200


# Comando di default (modificalo in base a cosa vuoi avviare)
# Per esempio, per far partire solo FastAPI:
# CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD tail -f /dev/null
