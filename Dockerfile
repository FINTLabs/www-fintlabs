FROM nginx:1.31.3-alpine-slim

COPY ./frontend/ /usr/share/nginx/html

EXPOSE 80