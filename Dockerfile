FROM nginx:1.31.1-alpine-slim

COPY ./frontend/ /usr/share/nginx/html

EXPOSE 80