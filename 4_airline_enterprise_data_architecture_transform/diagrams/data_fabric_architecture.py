#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.analytics import Hadoop, Spark
from diagrams.onprem.database import PostgreSQL, MongoDB, Cassandra
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import Users
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, Redshift, Dynamodb
from diagrams.aws.integration import SQS
from diagrams.azure.database import SQLDatabases, CosmosDb
from diagrams.azure.storage import BlobStorage
from diagrams.gcp.database import SQL
from diagrams.gcp.storage import GCS

# Create the diagram with a suitable title and configuration
with Diagram("Data Fabric Architecture", show=False, direction="TB", filename="data_fabric_architecture"):
    # User and application interfaces
    users = Users("Business Users")
    
    # Data access layer
    with Cluster("Data Access Layer"):
        api_gateway = Nginx("API Gateway")
        # Connect users to the API gateway
        users >> Edge(label="Query Data") >> api_gateway
    
    # Processing engine
    with Cluster("Processing Engine"):
        spark = Spark("Spark")
        hadoop = Hadoop("Hadoop")
    
    # Data governance and metadata
    with Cluster("Centralized Governance"):
        metadata = PostgreSQL("Metadata Repository")
        api_gateway >> Edge(label="Metadata Lookup") >> metadata
    
    # Data sources (on-premises)
    with Cluster("On-Premises Data"):
        postgres = PostgreSQL("PostgreSQL")
        mongo = MongoDB("MongoDB")
        cassandra = Cassandra("Cassandra")
        kafka = Kafka("Kafka")
        
        # Connect processing engine to on-prem data sources
        spark >> Edge(label="ETL") >> postgres
        spark >> mongo
        hadoop >> cassandra
        kafka >> Edge(label="Streaming") >> spark
    
    # Data sources (AWS)
    with Cluster("AWS"):
        s3 = S3("S3 Data Lake")
        rds = RDS("RDS")
        redshift = Redshift("Redshift")
        dynamodb = Dynamodb("DynamoDB")
        sqs = SQS("SQS")
        
        # Connect processing engine to AWS services
        spark >> Edge(label="Data Processing") >> s3
        hadoop >> rds
        spark >> redshift
        sqs >> Edge(label="Messages") >> spark
    
    # Data sources (Azure)
    with Cluster("Azure"):
        azure_sql = SQLDatabases("Azure SQL")
        cosmos = CosmosDb("Cosmos DB")
        blob = BlobStorage("Blob Storage")
        
        # Connect processing engine to Azure services
        spark >> azure_sql
        hadoop >> cosmos
        spark >> blob
    
    # Data sources (GCP)
    with Cluster("Google Cloud"):
        bigquery = SQL("BigQuery")
        gcs = GCS("Cloud Storage")
        
        # Connect processing engine to GCP services
        spark >> bigquery
        hadoop >> gcs
    
    # Connecting governance to all platforms
    metadata >> Edge(color="firebrick", style="dotted") >> spark
    metadata >> Edge(color="firebrick", style="dotted") >> hadoop
    
    # Connect API Gateway to processing engines
    api_gateway >> Edge(label="Query Federation") >> spark
    api_gateway >> hadoop