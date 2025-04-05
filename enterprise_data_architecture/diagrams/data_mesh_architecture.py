#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import PostgreSQL, MongoDB
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Istio
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Redshift
from diagrams.aws.storage import S3
from diagrams.custom import Custom

# Create the diagram
with Diagram("Data Mesh Architecture", show=False, direction="TB", filename="data_mesh_architecture"):
    
    # Data consumers
    users = Users("Data Consumers")
    
    # Data Mesh Discovery & Governance
    with Cluster("Discovery & Governance"):
        catalog = Custom("Data Catalog", "./resources/catalog.png")
        governance = Custom("Governance", "./resources/governance.png")
    
    # Domain-oriented data architecture
    with Cluster("Domain: Sales"):
        with Cluster("Sales Domain Data Product"):
            sales_api = Istio("Sales Data API")
            sales_db = PostgreSQL("Sales Database")
            sales_compute = Spark("Sales Analytics")
            
            sales_api >> sales_db
            sales_api << sales_compute >> sales_db
    
    with Cluster("Domain: Marketing"):
        with Cluster("Marketing Domain Data Product"):
            marketing_api = Istio("Marketing Data API")
            marketing_db = MongoDB("Marketing Database")
            marketing_compute = Lambda("Marketing Analytics")
            
            marketing_api >> marketing_db
            marketing_api << marketing_compute >> marketing_db
    
    with Cluster("Domain: Finance"):
        with Cluster("Finance Domain Data Product"):
            finance_api = Istio("Finance Data API")
            finance_db = Redshift("Finance Data Warehouse")
            finance_compute = Server("Finance Analytics")
            
            finance_api >> finance_db
            finance_api << finance_compute >> finance_db
    
    with Cluster("Domain: Customer"):
        with Cluster("Customer Domain Data Product"):
            customer_api = Istio("Customer Data API")
            customer_db = S3("Customer Data Lake")
            customer_stream = Kafka("Customer Events")
            
            customer_api >> customer_db
            customer_stream >> customer_db
    
    # Self-serve data platform
    with Cluster("Self-Serve Data Infrastructure"):
        platform = Custom("Data Platform", "./resources/platform.png")
        
    # Connect domains to governance, platform and users
    users >> Edge(label="Discover & Access") >> catalog
    catalog >> Edge(label="Register") << sales_api
    catalog >> Edge(label="Register") << marketing_api
    catalog >> Edge(label="Register") << finance_api
    catalog >> Edge(label="Register") << customer_api
    
    governance >> Edge(color="red", style="dotted") >> sales_api
    governance >> Edge(color="red", style="dotted") >> marketing_api
    governance >> Edge(color="red", style="dotted") >> finance_api
    governance >> Edge(color="red", style="dotted") >> customer_api
    
    platform >> Edge(color="blue", style="dotted") >> sales_api
    platform >> Edge(color="blue", style="dotted") >> marketing_api
    platform >> Edge(color="blue", style="dotted") >> finance_api
    platform >> Edge(color="blue", style="dotted") >> customer_api