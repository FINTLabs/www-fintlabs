FROM nginx:alpine-slim

COPY ./frontend/ /usr/share/nginx/html

EXPOSE 80