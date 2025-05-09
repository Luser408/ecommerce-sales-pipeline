import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource = glueContext.create_dynamic_frame.from_catalog(
    database="sales_db",
    table_name="raw",
    transformation_ctx="datasource"
)

df = datasource.toDF()
df_cleaned = df.dropDuplicates(['order_id']).na.drop(subset=['order_id'])
cleaned_dynamic_frame = DynamicFrame.fromDF(df_cleaned, glueContext, "cleaned_dynamic_frame")

glueContext.write_dynamic_frame.from_options(
    frame=cleaned_dynamic_frame,
    connection_type="s3",
    connection_options={"path": "s3://ecommerce-sales-pipeline-2025/cleaned/"},
    format="parquet",
    transformation_ctx="datasink"
)

job.commit()