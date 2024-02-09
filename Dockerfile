FROM python:3.10
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip


WORKDIR /django

COPY requirements.txt /django/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /django
COPY . /django/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django app
CMD ["gunicorn", "FoodOrdering.wsgi", "--bind", "0.0.0.0:8000", "--workers", "4"]