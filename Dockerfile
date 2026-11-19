ARG BASE=python:3.12-slim
FROM ${BASE}
ARG SERVICE=catalog
ARG BUILD_NUMBER=dev
ENV SERVICE=${SERVICE} APP_VERSION=${BUILD_NUMBER}
WORKDIR /app
COPY wheels ./wheels
RUN pip install --no-cache-dir --no-index --find-links=wheels flask gunicorn
COPY store ./store
EXPOSE 8000
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8000 store.${SERVICE}:app"]