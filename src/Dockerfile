FROM python:3.9-slim as compile-stage

# Install build tools
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

WORKDIR /app

# Switch to non-root user
RUN groupadd --gid 1000 appgroup && \
    useradd --create-home --gid 1000 --uid 1000 appuser
USER appuser

# Copy requirements to ensure that Docker will cache them
# instead of reinstalling them on every build
COPY requirements.txt .
RUN pip install --no-warn-script-location --user -r requirements.txt

# install uWSGI (not in requrements.txt as it is not needed
# in development/test environments):
RUN pip install --no-warn-script-location --user uwsgi


FROM python:3.9-slim

# Copy non-root user and group from compile stage
RUN groupadd --gid 1000 appgroup && \
    useradd --create-home --gid 1000 --uid 1000 appuser

# Copy compiled files
COPY --from=compile-stage /home/appuser/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

WORKDIR /app

# Copy codebase
COPY . .
EXPOSE 5000

# Set environment flags
ENV FLASK_APP=manage.py
ENV FLASK_ENV=production

# Change owner of DB files to allow writing
RUN chown -R appuser:appgroup buddy_recommender/main/storage

# Change user to non-root
USER appuser

# Run migrations script
RUN python manage.py db upgrade

# Run server
CMD ["uwsgi", "/app/wsgi.ini", "-w", "wsgi:app"]
