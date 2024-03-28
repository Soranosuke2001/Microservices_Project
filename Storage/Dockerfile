FROM python:latest

# Set maintainer label using the conventional format
LABEL maintainer="sschlegel1@my.bcit.ca"

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8090 available to the world outside this container
EXPOSE 8090

# Copy entrypoint script into the container and make it executable
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Run entrypoint.sh when the container launches
ENTRYPOINT ["entrypoint.sh"]

# FROM python:latest

# LABEL maintainer = "sschlegel1@my.bcit.ca"

# WORKDIR /app
# COPY . .

# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8090

# CMD python create_database.py && python app.py

# Use a specific version of the Python image to ensure consistency
