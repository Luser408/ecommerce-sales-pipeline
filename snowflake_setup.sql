CREATE TABLE ECOMMERCE_DB.SALES.ORDERS (
    order_id STRING,
    product_id STRING,
    product_category STRING,
    price FLOAT,
    order_date TIMESTAMP
);

USE ROLE ACCOUNTADMIN;
CREATE STORAGE INTEGRATION s3_integration
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = S3
    ENABLED = TRUE
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::559050227340:role/pipeline-role'
    STORAGE_ALLOWED_LOCATIONS = ('s3://ecommerce-sales-pipeline-2025/cleaned/');

USE DATABASE ECOMMERCE_DB;
USE SCHEMA SALES;
CREATE STAGE s3_cleaned_stage
    STORAGE_INTEGRATION = s3_integration
    URL = 's3://ecommerce-sales-pipeline-2025/cleaned/'
    FILE_FORMAT = (TYPE = PARQUET);

CREATE PIPE sales_pipe
    AUTO_INGEST = TRUE
    AS
    COPY INTO ORDERS (order_id, product_id, product_category, price, order_date)
    FROM (
        SELECT
            $1:order_id::STRING,
            $1:product_id::STRING,
            $1:product_category::STRING,
            $1:price::FLOAT,
            $1:order_date::TIMESTAMP
        FROM @s3_cleaned_stage
    )
    FILE_FORMAT = (TYPE = PARQUET);