import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1739427923182 = glueContext.create_dynamic_frame.from_catalog(database="nyimaglue", table_name="tabletesttest__1__csv", transformation_ctx="AWSGlueDataCatalog_node1739427923182")

# Script generated for node Drop Fields
DropFields_node1739428197939 = DropFields.apply(frame=AWSGlueDataCatalog_node1739427923182, paths=[], transformation_ctx="DropFields_node1739428197939")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=DropFields_node1739428197939, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1739427837127", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1739428237455 = glueContext.write_dynamic_frame.from_options(frame=DropFields_node1739428197939, connection_type="s3", format="glueparquet", connection_options={"path": "s3://glue-bucket-nyima/output/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1739428237455")

job.commit()