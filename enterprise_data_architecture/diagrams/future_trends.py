#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.generic.compute import Rack
from diagrams.onprem.client import Users
from diagrams.aws.ml import Sagemaker
from diagrams.aws.compute import Lambda
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.gcp.ml import AIPlatform
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.flowchart import Action, Decision
from diagrams.aws.storage import S3
from diagrams.custom import Custom
from diagrams.aws.general import General

# Create the diagram for future trends in enterprise data architecture
with Diagram("Future Trends in Enterprise Data Architecture", show=False, direction="TB", filename="future_trends"):
    
    # Central data mesh concept
    with Cluster("Next-Gen Data Architecture"):
        mesh_core = Rack("Evolutionary Architecture")
        
        # Connect various emerging technologies around the core
        with Cluster("AI-Driven Architecture"):
            ai_engine = Sagemaker("Foundation Models")
            ai_agents = Lambda("Intelligent Agents")
            ai_analytics = MachineLearningServiceWorkspaces("Automated Analytics")
            
            ai_engine - ai_agents - ai_analytics
        
        with Cluster("Decentralized Data Ecosystems"):
            domain_products = General("Data Products")
            governance = PostgreSQL("Federated Governance")
            collaboration = Users("Cross-Domain Collaboration")
            
            domain_products - governance - collaboration
        
        with Cluster("Real-Time & Event Architecture"):
            streaming = Spark("Stream Processing")
            events = Custom("Event Backbone", "./enterprise_data_architecture/diagrams/resources/catalog.png")
            decisions = AIPlatform("Real-time Decisions")
            
            streaming >> events >> decisions
        
        with Cluster("DataOps & Automation"):
            cicd = Decision("CI/CD Pipelines")
            testing = Action("Automated Testing")
            deployment = Action("Self-Service Deployment")
            
            cicd >> testing >> deployment
            
        with Cluster("Data Sustainability"):
            storage_opt = S3("Storage Optimization")
            carbon = Custom("Carbon Footprint", "./enterprise_data_architecture/diagrams/resources/catalog.png")
            lifecycle = Action("Data Lifecycle")
            
            storage_opt - carbon - lifecycle
    
    # Connect everything to the core
    ai_engine >> mesh_core
    domain_products >> mesh_core
    streaming >> mesh_core
    cicd >> mesh_core
    storage_opt >> mesh_core