FROM nginx:1.30.0-alpine-slim

COPY ./frontend/ /usr/share/nginx/html

EXPOSE 80