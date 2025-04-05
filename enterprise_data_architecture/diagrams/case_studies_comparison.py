#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL, MongoDB, Cassandra
from diagrams.onprem.network import Internet
from diagrams.onprem.analytics import Spark, Hadoop
from diagrams.aws.storage import S3
from diagrams.aws.database import Redshift, Dynamodb
from diagrams.azure.database import CosmosDb
from diagrams.gcp.analytics import BigQuery
from diagrams.custom import Custom

# Create the diagram for case studies comparison
with Diagram("Enterprise Data Architecture Case Studies Comparison", show=False, direction="TB", filename="case_studies_comparison"):
    
    # Central Users/Consumers
    users = Users("Data Consumers")
    
    with Cluster("Financial Services Case Study"):
        with Cluster("Hybrid Architecture"):
            fin_data_lake = S3("Data Lake")
            fin_warehouse = Redshift("Data Warehouse")
            fin_streaming = Custom("Event Processing", "./enterprise_data_architecture/diagrams/resources/catalog.png")
            
            fin_data_lake - fin_warehouse
            fin_streaming >> fin_data_lake
    
    with Cluster("Healthcare Case Study"):
        with Cluster("Data Mesh Implementation"):
            health_domain1 = Custom("Patient Domain", "./enterprise_data_architecture/diagrams/resources/catalog.png")
            health_domain2 = Custom("Clinical Domain", "./enterprise_data_architecture/diagrams/resources/catalog.png")
            health_domain3 = Custom("Research Domain", "./enterprise_data_architecture/diagrams/resources/catalog.png")
            health_governance = PostgreSQL("Governance")
            
            health_domain1 - health_domain2 - health_domain3
            health_governance >> Edge(style="dotted") >> health_domain1
            health_governance >> Edge(style="dotted") >> health_domain2
            health_governance >> Edge(style="dotted") >> health_domain3
    
    with Cluster("Retail Case Study"):
        with Cluster("Data Fabric Implementation"):
            retail_central = Internet("Central Integration")
            retail_store = PostgreSQL("Store Data")
            retail_online = MongoDB("Online Data")
            retail_analytics = Spark("Analytics Engine")
            
            retail_store >> retail_central
            retail_online >> retail_central
            retail_central >> retail_analytics
    
    with Cluster("Manufacturing Case Study"):
        with Cluster("IoT Data Architecture"):
            mfg_devices = Custom("IoT Devices", "./enterprise_data_architecture/diagrams/resources/catalog.png")
            mfg_streaming = Cassandra("Streaming Store")
            mfg_processing = Spark("Real-time Processing")
            mfg_storage = Hadoop("Historical Store")
            
            mfg_devices >> mfg_streaming >> mfg_processing
            mfg_processing >> mfg_storage
            
    # Connect to central users node
    fin_warehouse >> Edge(color="blue") >> users
    health_domain1 >> Edge(color="green") >> users
    retail_analytics >> Edge(color="red") >> users
    mfg_processing >> Edge(color="orange") >> users