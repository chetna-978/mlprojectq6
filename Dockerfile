FROM python:3.8-alpine

# Copy the application code to the /app directory
RUN mkdir /app
COPY . /app/
WORKDIR /app/

# Install the required Python packages
RUN pip3 install -r requirements.txt

# Install Apache Airflow
RUN pip3 install apache-airflow

# Set the environment variables for Airflow
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True

# Initialize the Airflow database
RUN airflow db init

# Create an Airflow admin user
RUN airflow users create -e YOUR_EMAIL -f YOUR_FIRST_NAME -l YOUR_LAST_NAME -p YOUR_PASSWORD -r Admin -u admin

# Install the AWS CLI
RUN apt update -y && apt install awscli -y

# Set the entrypoint and command for the Docker container
CMD ["python", "app.py"]
