FROM nginx:1.31.3-alpine-slim

ARG BUILD_VERSION=development

COPY ./frontend/ /usr/share/nginx/html/

RUN sed -i "s/__BUILD_VERSION__/${BUILD_VERSION}/g" \
    /usr/share/nginx/html/index.html

EXPOSE 80