#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.analytics import Spark
from diagrams.onprem.queue import Kafka
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.programming.framework import React

with Diagram("Implementation Roadmap", show=False, filename="implementation_roadmap"):
    
    with Cluster("Phase 1: Foundation"):
        p1 = Users("Stakeholder Alignment")
        p2 = Server("Domain Identification")
        p3 = PostgreSQL("Initial Data Catalog")
        
        p1 >> Edge(label="3 months") >> p2
        p2 >> Edge(label="2 months") >> p3
    
    with Cluster("Phase 2: Core Components"):
        p4 = Kafka("Event Streaming")
        p5 = Airflow("Data Pipeline Orchestration")
        p6 = Spark("Processing Framework")
        
        p3 >> Edge(label="4 months") >> p4
        p4 >> p5
        p5 >> p6
    
    with Cluster("Phase 3: Domain Integration"):
        p7 = Server("Domain APIs")
        p8 = Nginx("API Gateway")
        p9 = React("Self-service Portal")
        
        p6 >> Edge(label="6 months") >> p7
        p7 >> p8
        p8 >> p9
    
    with Cluster("Phase 4: Optimization"):
        p10 = Prometheus("Monitoring")
        p11 = Grafana("Analytics Dashboard")
        p12 = Users("Federated Governance")
        
        p9 >> Edge(label="3 months") >> p10
        p10 >> p11
        p11 >> p12