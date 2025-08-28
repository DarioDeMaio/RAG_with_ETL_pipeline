FROM node:20-bullseye

WORKDIR /app

COPY . .

RUN npm install -g @angular/cli

# CMD ["sleep", "infinity"]

CMD ["ng", "serve", "--host", "0.0.0.0", "--port", "4300"]
