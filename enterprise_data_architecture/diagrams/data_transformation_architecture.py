#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Glue, Athena, Quicksight
from diagrams.aws.database import Redshift, Dynamodb
from diagrams.aws.compute import Lambda
from diagrams.onprem.analytics import Spark
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Python
from diagrams.programming.flowchart import Document

with Diagram("Data Transformation Architecture", show=False, direction="LR", filename="data_transformation_architecture"):
    
    # Raw Data Sources
    with Cluster("Raw Data Layer"):
        raw_storage = S3("Raw Data Lake")
        document_store = Document("Unstructured Data")
        relational_db = PostgreSQL("Structured Data")
    
    # ETL and Transformation Layer
    with Cluster("Transformation Layer"):
        etl_engine = Glue("ETL Engine")
        stream_processing = Spark("Stream Processing")
        batch_processing = Lambda("Batch Processing")
        workflow_orchestration = Airflow("Pipeline Orchestration")
        data_quality = Python("Data Quality Checks")
    
    # Processed Data Layer
    with Cluster("Processed Data Layer"):
        processed_storage = S3("Processed Data Lake")
        data_warehouse = Redshift("Data Warehouse")
        metadata_store = Dynamodb("Metadata Catalog")
    
    # Analytics and Consumption Layer
    with Cluster("Analytics Layer"):
        query_engine = Athena("SQL Query Engine")
        visualization = Quicksight("Data Visualization")
    
    # Data Flow
    raw_storage >> etl_engine
    document_store >> etl_engine
    relational_db >> etl_engine
    
    etl_engine >> workflow_orchestration
    stream_processing >> workflow_orchestration
    batch_processing >> workflow_orchestration
    
    workflow_orchestration >> data_quality
    data_quality >> processed_storage
    data_quality >> data_warehouse
    
    processed_storage >> metadata_store
    data_warehouse >> metadata_store
    
    processed_storage >> query_engine
    data_warehouse >> query_engine
    query_engine >> visualization
    
    # Feedback Loop
    visualization >> Edge(color="red", style="dashed", label="Refinement") >> workflow_orchestration