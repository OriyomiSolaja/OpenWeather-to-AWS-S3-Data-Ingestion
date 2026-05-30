import json
import os
import logging
import boto3
import requests
from datetime import datetime, timezone

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
s3 = boto3.client("s3")
secrets_client = boto3.client("secretsmanager")

# Configuration
BUCKET_NAME = os.environ.get("BUCKET_NAME", "weather-data-lake234")
CITY = os.environ.get("CITY", "London")
SECRET_NAME = os.environ.get("SECRET_NAME", "weather/api")


def get_secret():
    """Retrieve Weather API key from AWS Secrets Manager."""

    response = secrets_client.get_secret_value(
        SecretId=SECRET_NAME
    )

    secret = json.loads(response["SecretString"])

    return secret["weather_api_key"]


def lambda_handler(event, context):
    try:
        logger.info("Weather extraction started")

        # Get API key securely
        api_key = get_secret()

        # Weather API URL
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={CITY}&appid={api_key}&units=metric"
        )

        # Call Weather API
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Convert response to JSON
        weather_data = response.json()

        # Create UTC timestamp
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y%m%d_%H%M%S")

        # Add ingestion metadata
        weather_data["ingestion_metadata"] = {
            "ingestion_timestamp_utc": now.isoformat(),
            "source_system": "OpenWeather API",
            "pipeline_name": "weather_lambda_to_s3",
            "city": CITY
        }

        # Partitioned S3 file path
        file_name = (
            f"weather_data/"
            f"year={now.strftime('%Y')}/"
            f"month={now.strftime('%m')}/"
            f"day={now.strftime('%d')}/"
            f"weather_{CITY.lower()}_{timestamp}.json"
        )

        # Upload JSON to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(weather_data),
            ContentType="application/json"
        )

        logger.info(f"Weather data uploaded successfully to {file_name}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Weather data uploaded successfully",
                "bucket": BUCKET_NAME,
                "file_name": file_name
            })
        }

    except requests.exceptions.RequestException as api_error:
        logger.error(f"Weather API request failed: {str(api_error)}")
        raise

    except Exception as error:
        logger.error(f"Lambda execution failed: {str(error)}")
        raise