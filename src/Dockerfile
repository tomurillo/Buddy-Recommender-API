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

# Copy and run codebase
COPY . /app
EXPOSE 5000

USER app

ENTRYPOINT ["uwsgi"]
CMD ["wsgi.ini", "-w", "wsgi:app"]
