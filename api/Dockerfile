ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-alpine as builder
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /tmp
RUN apk add gcc python3-dev libc-dev libffi-dev
RUN pip install -q --upgrade pip pipenv
COPY Pipfile Pipfile.lock /tmp/
RUN pipenv requirements > requirements.txt && \
    python -m venv /opt/venv && \
    pip install -q -r requirements.txt

FROM python:${PYTHON_VERSION}-alpine as runner
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . .
CMD uvicorn app:app --host 0.0.0.0 --port 80
