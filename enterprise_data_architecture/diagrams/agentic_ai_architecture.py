#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import Comprehend, Rekognition, SagemakerModel
from diagrams.onprem.client import Users
from diagrams.programming.framework import React
from diagrams.aws.integration import SNS
from diagrams.aws.database import Dynamodb
from diagrams.generic.compute import Rack

with Diagram("Agentic AI Data Architecture", show=False, direction="LR", filename="agentic_ai_architecture"):
    
    # User interface
    user = Users("Business Users")
    ui = React("Interactive UI")
    
    # Agent Orchestration
    with Cluster("Agent Orchestration Layer"):
        orchestrator = Rack("Agent Orchestrator")
        planner = Lambda("Task Planning")
        memory = Dynamodb("Agent Memory")
        notification = SNS("Notification Service")
    
    # AI Services and Models
    with Cluster("AI Services and Models"):
        nlp = Comprehend("NLP Service")
        vision = Rekognition("Computer Vision")
        ml_models = SagemakerModel("Custom ML Models")
    
    # Data Layer
    with Cluster("Enterprise Data Layer"):
        data_lake = S3("Data Lake")
        data_catalog = Dynamodb("Data Catalog")
    
    # Workflow
    user >> ui >> orchestrator
    
    # Orchestration connections
    orchestrator >> planner
    orchestrator >> memory
    orchestrator >> notification
    
    # AI services connections
    orchestrator >> nlp
    orchestrator >> vision
    orchestrator >> ml_models
    
    # Data connections
    nlp >> data_lake
    vision >> data_lake
    ml_models >> data_lake
    
    # Fix the connection between data_lake and data_catalog
    data_lake >> data_catalog
    
    # Notification path
    notification >> ui
    
    # Feedback loop
    ui >> Edge(color="green", style="dashed", label="Feedback") >> memory