# E-commerce Sales Pipeline

A robust, automated data pipeline leveraging **AWS** (S3, Lambda, Glue) and **Snowflake** to process and analyze e-commerce sales data. This project ingests raw CSV files, cleans and transforms them into Parquet format, and loads them into a Snowflake data warehouse for analytics.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Project Files](#project-files)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview
This pipeline automates the ingestion, transformation, and storage of e-commerce sales data. Raw CSV files uploaded to an S3 bucket trigger a Lambda function, which initiates an AWS Glue job to clean and convert the data into Parquet files. Snowflake’s Snowpipe then loads the Parquet files into a data warehouse for querying and analysis.

## Architecture
The pipeline consists of the following components:
- **AWS S3**: Stores raw CSV files in the `raw/` prefix and cleaned Parquet files in the `cleaned/` prefix of the `ecommerce-sales-pipeline-2025` bucket.
- **AWS Lambda**: A `sales_trigger` function monitors the `raw/` prefix and triggers the Glue job on new uploads.
- **AWS Glue**: A `sales_cleaning_job` processes raw data, removes duplicates, handles missing values, and saves Parquet files to `cleaned/`.
- **Snowflake Snowpipe**: Automatically loads Parquet files from `cleaned/` into the `ECOMMERCE_DB.SALES.ORDERS` table.

## Prerequisites
- AWS account with permissions to create S3 buckets, Lambda functions, Glue jobs, and IAM roles.
- Snowflake account with administrative privileges.
- Local environment with AWS CLI configured.
- Basic knowledge of Python, SQL, and cloud data pipelines.

## Setup Instructions
1. **Create S3 Bucket**:
   - Create a bucket named `ecommerce-sales-pipeline-2025` with `raw/` and `cleaned/` prefixes.
2. **Set Up IAM Role**:
   - Create a role `pipeline-role` with policies: `AmazonS3FullAccess`, `AWSGlueServiceRole`, and `AWSLambdaBasicExecutionRole`.
3. **Configure AWS Lambda**:
   - Create a function `sales_trigger` using `lambda_function.py`.
   - Add an S3 trigger for the `raw/` prefix.
4. **Set Up AWS Glue**:
   - Create a crawler `sales_crawler` to catalog data in `raw/`.
   - Create a job `sales_cleaning_job` using `sales_cleaning_job.py`.
5. **Configure Snowflake**:
   - Run `snowflake_setup.sql` to create the `ORDERS` table, S3 integration, stage, and Snowpipe.
6. **Test Pipeline**:
   - Upload a CSV file (e.g., `test_sales_6.csv`) to `s3://ecommerce-sales-pipeline-2025/raw/`.
   - Verify Parquet files in `cleaned/` and data in Snowflake’s `ORDERS` table.

## Project Files
- **`lambda_function.py`**: Python script for the Lambda function that triggers the Glue job.
- **`sales_cleaning_job.py`**: Python script for the Glue job to clean and transform data.
- **`snowflake_setup.sql`**: SQL script to set up Snowflake table, stage, and Snowpipe.
- **`README.md`**: Project documentation (this file).

## Usage
1. Upload e-commerce sales data as CSV files to `s3://ecommerce-sales-pipeline-2025/raw/`.
2. The pipeline automatically processes files and loads data into Snowflake.
3. Query the `ECOMMERCE_DB.SALES.ORDERS` table in Snowflake for analysis:
   ```sql
   SELECT * FROM ECOMMERCE_DB.SALES.ORDERS LIMIT 5;
