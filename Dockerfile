FROM nginx:1.31.5-alpine-slim

ARG BUILD_VERSION=development

COPY ./frontend/ /usr/share/nginx/html/
COPY ./nginx.conf /etc/nginx/conf.d/default.conf 

RUN sed -i "s/__BUILD_VERSION__/${BUILD_VERSION}/g" \
    /usr/share/nginx/html/index.html \
    && nginx -t

EXPOSE 80