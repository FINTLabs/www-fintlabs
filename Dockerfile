FROM python:3.13-alpine AS security-check

WORKDIR /site
COPY ./frontend/ ./frontend/
COPY ./security/ ./security/
COPY ./scripts/security.py ./scripts/security.py
COPY ./security-headers.conf ./security-headers.conf
COPY ./tests/ ./tests/
RUN python3 -m unittest discover -s tests -v \
    && python3 scripts/security.py --check

FROM nginx:1.31.8-alpine-slim

ARG BUILD_VERSION=development

COPY --from=security-check /site/frontend/ /usr/share/nginx/html/
COPY ./nginx.conf /etc/nginx/conf.d/default.conf 
COPY --from=security-check /site/security-headers.conf /etc/nginx/security-headers.conf

RUN sed -i "s/__BUILD_VERSION__/${BUILD_VERSION}/g" \
    /usr/share/nginx/html/index.html \
    && nginx -t

EXPOSE 80
