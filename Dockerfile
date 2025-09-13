# Start with a lightweight and official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the file that lists the dependencies
COPY requirements.txt .

# Install the dependencies. Using --no-cache-dir reduces the image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# Let the container platform (like Render) tell us which port to listen on.
# Default to 8080 if the PORT variable is not set.
ENV PORT 8080

# The command to run your application using the Gunicorn web server.
# It listens on all network interfaces (0.0.0.0) and on the port specified by the $PORT env var.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
