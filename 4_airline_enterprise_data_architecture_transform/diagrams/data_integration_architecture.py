#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import MongoDB, PostgreSQL
from diagrams.onprem.analytics import Spark, Hadoop
from diagrams.onprem.client import Users
from diagrams.programming.framework import Spring, React
from diagrams.aws.integration import Eventbridge, SQS, SNS
from diagrams.aws.analytics import Glue
from diagrams.aws.storage import S3
from diagrams.aws.database import Redshift

with Diagram("Data Integration Architecture", show=False, direction="TB", filename="data_integration_architecture"):
    
    # Source Systems
    with Cluster("Source Systems"):
        source_db1 = PostgreSQL("Transactional DB")
        source_db2 = MongoDB("NoSQL DB")
        source_app = Spring("Source Application")
    
    # Data Integration Layer
    with Cluster("Data Integration Layer"):
        # Event-driven ingestion
        ingestion_bus = Kafka("Event Bus")
        
        # Batch ETL
        batch_etl = Glue("ETL Pipeline")
        
        # API Gateway
        api_gateway = Spring("API Gateway")
        
        # Message Queue
        message_queue = SQS("Message Queue")
        
        # Event Router
        event_router = Eventbridge("Event Router")
    
    # Data Processing
    with Cluster("Data Processing"):
        spark = Spark("Stream Processing")
        batch = Hadoop("Batch Processing")
    
    # Target Data Stores
    with Cluster("Target Data Stores"):
        data_lake = S3("Data Lake")
        data_warehouse = Redshift("Data Warehouse")
        operational_db = PostgreSQL("Operational Data")
    
    # Data Consumers
    with Cluster("Data Consumers"):
        analytics = React("Analytics Dashboard")
        notifications = SNS("Notifications")
        users = Users("Business Users")
    
    # Source to Integration connections
    source_db1 >> batch_etl
    source_db2 >> batch_etl
    source_app >> ingestion_bus
    source_app >> api_gateway
    source_app >> message_queue
    
    # Integration to Processing connections
    ingestion_bus >> spark
    batch_etl >> batch
    api_gateway >> spark
    message_queue >> spark
    event_router >> spark
    
    # Processing to Target connections
    spark >> data_lake
    spark >> operational_db
    batch >> data_lake
    batch >> data_warehouse
    
    # Target to Consumer connections
    data_lake >> analytics
    data_warehouse >> analytics
    operational_db >> notifications
    
    analytics >> users
    notifications >> users