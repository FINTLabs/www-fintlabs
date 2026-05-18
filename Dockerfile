FROM nginx:1.31.0-alpine-slim

COPY ./frontend/ /usr/share/nginx/html

EXPOSE 80