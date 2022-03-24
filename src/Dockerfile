FROM python:3

RUN groupadd --gid 1000 app && \
    useradd --create-home --gid 1000 --uid 1000 app

WORKDIR /app

# Copy requirements to ensure that Docker will cache them
# instead of reinstalling them on every build
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# install uWSGI (not in requrements.txt as it is not needed
# in development/test environments):
RUN pip install uwsgi

# Copy codebase
COPY . .
EXPOSE 5000

# Set environment flags
ENV FLASK_APP=manage.py
ENV FLASK_ENV=production

# Add DB directory
RUN mkdir buddy_recommender/main/storage
# Run migrations script
RUN python manage.py db upgrade
# Change owner of DB files to allow writing
RUN chown -R app:app buddy_recommender/main/storage

# Change user to non-root
USER app

# Run server
CMD ["uwsgi", "wsgi.ini", "-w", "wsgi:app"]
