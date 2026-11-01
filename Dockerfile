FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    HOME=/tmp
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt \
    && useradd --uid 1001 --gid 0 --no-create-home accounts
COPY --chown=1001:0 service ./service
# UID 1001 locally; OpenShift may replace it with an arbitrary unprivileged UID.
RUN chgrp -R 0 /app && chmod -R g=u /app
USER 1001
EXPOSE 8080
ENTRYPOINT ["gunicorn"]
CMD ["--bind=0.0.0.0:8080", "--workers=1", "--threads=4", "--access-logfile=-", "--error-logfile=-", "service:app"]
