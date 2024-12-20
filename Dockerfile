# Use the official Python image as the base
# FROM python:3.9-slim
FROM bitnami/spark:3.3.1


USER root




# Set the working directory inside the container
WORKDIR /opt/app


# Copy the requirements file to the working directory
COPY requirements.txt .


RUN apt-get update && apt-get install -y zip && rm -rf /var/lib/apt/lists/*



# Install Python dependencies
RUN pip install  -r requirements.txt

# Copy the entire application code to the working directory
# COPY . .
COPY ./app /opt/app

RUN zip -r /opt/app.zip /opt/app


RUN mkdir -p /app/tmp && chmod -R 777 /app/tmp


# Set the default command to run the script
CMD ["python", "/opt/app/main.py", "20"]
