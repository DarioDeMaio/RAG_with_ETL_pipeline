FROM node:20 AS build

WORKDIR /frontend

RUN npm install -g @angular/cli

COPY package*.json ./

RUN npm install

COPY  . .

RUN ng build --configuration production

FROM nginx:alpine

COPY --from=build /frontend/dist/* /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]