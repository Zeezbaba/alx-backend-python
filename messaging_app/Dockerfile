# Use base python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt file first
COPY Requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r Requirements.txt

# Copy the rest of the project code
COPY . .

# Expose django default port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]