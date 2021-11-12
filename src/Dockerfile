FROM python:3.9.1
WORKDIR /app

# Copy requirements to enure that Docker will cache them instead of reinstall them
# on every build
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy and run codebase
COPY . /app
EXPOSE 8000
CMD ["python", "manage.py", "run", "0.0.0.0:8000"]
