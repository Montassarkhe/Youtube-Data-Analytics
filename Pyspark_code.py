import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from awsglue.dynamicframe import DynamicFrame


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

#convert all the lunguage to the utf code format
predicate_pushdown = "region in ('ca','gb','us')"

datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "youtuberaw", table_name = "raw_statistics", transformation_ctx = "datasource0", push_down_predicate = predicate_pushdown)


# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": ["s3://youtubedatanlyticsbucket/youtube/raw_statistics/"],
        "recurse": True,
    },
    transformation_ctx="S3bucket_node1",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=S3bucket_node1,
    mappings=[
        ("video_id", "string", "video_id", "bigint"),
        ("trending_date", "string", "trending_date", "string"),
        ("title", "string", "title", "string"),
        ("channel_title", "string", "channel_title", "string"),
        ("category_id", "string", "category_id", "bigint"),
        ("publish_time", "string", "publish_time", "string"),
        ("tags", "string", "tags", "string"),
        ("views", "string", "views", "string"),
        ("likes", "string", "likes", "bigint"),
        ("dislikes", "string", "dislikes", "bigint"),
        ("comment_count", "string", "comment_count", "bigint"),
        ("thumbnail_link", "string", "thumbnail_link", "string"),
        ("comments_disabled", "string", "comments_disabled", "boolean"),
        ("ratings_disabled", "string", "ratings_disabled", "boolean"),
        ("video_error_or_removed", "string", "video_error_or_removed", "boolean"),
        ("description", "string", "description", "string"),
    ],
    transformation_ctx="ApplyMapping_node2",
)
#modified by montassar
# Script generated for node S3 bucket
S3bucket_node3 = glueContext.write_dynamic_frame.from_options(
    frame=S3bucket_node1,
    connection_type="s3",
    format="glueparquet",
    connection_options={"path": "s3://youtubecleanedbucket", "partitionKeys": ["region"]},
    transformation_ctx="S3bucket_node3",
)

job.commit()
