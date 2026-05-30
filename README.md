# OpenWeather API to AWS S3 Data Ingestion Pipeline

## Project Overview

This project demonstrates a serverless cloud-based data ingestion pipeline built on AWS. The solution automatically extracts real-time weather data from the OpenWeather API, securely processes the data using AWS Lambda, and stores raw JSON files in Amazon S3 for future analytics and warehousing.

The project was developed to practice real-world cloud data engineering concepts including:
- Serverless architecture
- Event-driven processing
- Secure secret management
- Cloud-native deployment
- Automated scheduling
- Data lake ingestion patterns

---
```markdown

# Architecture

<p align="center">
  <a href="images/architecture-diagram.png">
    <img src="images/architecture-diagram.png" width="800">
  </a>
</p>

```

---

# Solution Components

| Component | Purpose |
|---|---|
| VS Code + AWS Toolkit | Local development and deployment |
| AWS SAM | Infrastructure as Code (IaC) deployment |
| AWS CloudFormation | Provisioning AWS resources |
| EventBridge Scheduler | Automatically triggers Lambda every hour |
| AWS Lambda | Extracts and processes weather data |
| AWS Secrets Manager | Securely stores API keys |
| OpenWeather API | External weather data source |
| Amazon S3 | Stores raw JSON weather data |
| CloudWatch Logs | Monitoring and troubleshooting |

---

# Key Features

- Automated hourly weather data ingestion
- Secure API key retrieval using AWS Secrets Manager
- Event-driven serverless architecture
- Partitioned S3 storage structure
- Cloud-native monitoring using CloudWatch
- Infrastructure deployment using AWS SAM
- Retry handling using EventBridge Scheduler
- Environment variable configuration

---

# Data Flow

1. EventBridge Scheduler triggers the Lambda function every hour.
2. Lambda retrieves the weather API key from AWS Secrets Manager.
3. Lambda sends a request to the OpenWeather API.
4. Weather data is returned in JSON format.
5. Lambda enriches the data with ingestion metadata.
6. The JSON file is uploaded into Amazon S3.
7. CloudWatch Logs captures execution logs and errors.

---

# S3 Storage Structure

The project uses a partitioned S3 folder structure for scalability and future analytics optimisation.

```text
weather_data/
    year=2026/
        month=05/
            day=30/
                weather_london_20260530_120000.json
```

---

# Technologies Used

| Technology | Usage |
|---|---|
| Python 3.12 | Lambda function development |
| AWS Lambda | Serverless compute |
| Amazon S3 | Cloud object storage |
| AWS SAM | Infrastructure deployment |
| AWS Secrets Manager | Secret storage |
| Amazon EventBridge Scheduler | Automated scheduling |
| Amazon CloudWatch | Logging and monitoring |
| OpenWeather API | External weather API |
| VS Code | Development environment |

---

# Security Implementation

The project follows cloud security best practices:

- API keys are stored securely in AWS Secrets Manager
- No credentials are hardcoded in source code
- IAM least-privilege access policies are used
- Sensitive files are excluded using `.gitignore`
- Environment variables are used for configuration

---

# IAM Permissions

The Lambda execution role includes permissions for:
- Writing weather files to Amazon S3
- Retrieving secrets from AWS Secrets Manager
- Writing logs to CloudWatch

---

# Deployment Process

The solution is deployed using AWS SAM.

## Validate Template

```bash
sam validate
```

## Build Application

```bash
sam build
```

## Deploy Infrastructure

```bash
sam deploy --guided --region us-east-1
```

---

# EventBridge Scheduler Configuration

The Lambda function is triggered automatically using:

```yaml
ScheduleExpression: rate(1 hour)
```

Retry policy:

```yaml
RetryPolicy:
  MaximumRetryAttempts: 2
  MaximumEventAgeInSeconds: 3600
```

---

# Environment Variables

| Variable | Purpose |
|---|---|
| BUCKET_NAME | S3 bucket name |
| CITY | Weather city |
| SECRET_NAME | Secrets Manager secret name |

---

# Monitoring

CloudWatch Logs is used to:
- Monitor Lambda executions
- Track API failures
- Monitor ingestion success
- Troubleshoot deployment/runtime issues

---

# Example KPIs

The ingested weather data can be used to measure:

| KPI | Description |
|---|---|
| Average Temperature | Daily average weather |
| Humidity Trends | Moisture tracking |
| Wind Speed | Wind behaviour analysis |
| API Success Rate | Ingestion reliability |
| Lambda Execution Duration | Pipeline performance |
| Data Freshness | Latest successful ingestion |
| File Volume Growth | Storage monitoring |

---

# Future Enhancements

Planned improvements include:

- Amazon Redshift integration
- AWS Glue Crawler and Data Catalog
- Amazon Athena querying
- JSON to Parquet conversion
- Power BI dashboard integration
- CI/CD with GitHub Actions
- SNS alert notifications
- Medallion data lake architecture

---

# Learning Outcomes

This project demonstrates practical experience in:
- AWS serverless architecture
- Event-driven systems
- Infrastructure as Code
- Cloud security
- Data lake ingestion
- Automated cloud deployment
- Cloud-native monitoring
- Modern data engineering practices

---

# Author

**Oriyomi Solaja**  
Data Analyst | Business Data Analyst | Cloud & Data Engineering Enthusiast

GitHub Repository:  
https://github.com/OriyomiSolaja/OpenWeather-to-AWS-S3-Data-Ingestion

