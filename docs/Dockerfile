FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install mkdocs + theme(s)
RUN pip install --no-cache-dir \
    mkdocs \
    mkdocs-material \
    pymdown-extensions

WORKDIR /site

# Copy mkdocs config and content
COPY mkdocs.yml .
COPY docs ./docs

EXPOSE 8000

CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
