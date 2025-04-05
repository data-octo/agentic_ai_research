#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.database import MongoDB, PostgreSQL, MySQL
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import Spring, Flask
from diagrams.programming.language import Java, Python

with Diagram("Domain-Driven Design Architecture", show=False, direction="TB", filename="domain_driven_design"):
    
    # Event Bus
    kafka = Kafka("Domain Event Bus")
    
    # Bounded Contexts
    with Cluster("Customer Management Bounded Context"):
        with Cluster("Hexagonal Architecture"):
            customer_api = Nginx("Customer API")
            
            with Cluster("Domain Layer"):
                customer_domain = Java("Customer Domain")
            
            with Cluster("Application Layer"):
                customer_app = Spring("Customer Service")
            
            with Cluster("Infrastructure Layer"):
                customer_db = PostgreSQL("Customer DB")
            
            customer_api >> customer_app >> customer_domain
            customer_domain >> customer_app >> customer_db
    
    with Cluster("Order Management Bounded Context"):
        with Cluster("Hexagonal Architecture"):
            order_api = Nginx("Order API")
            
            with Cluster("Domain Layer"):
                order_domain = Java("Order Domain")
            
            with Cluster("Application Layer"):
                order_app = Spring("Order Service")
            
            with Cluster("Infrastructure Layer"):
                order_db = MySQL("Order DB")
            
            order_api >> order_app >> order_domain
            order_domain >> order_app >> order_db
    
    with Cluster("Inventory Management Bounded Context"):
        with Cluster("Hexagonal Architecture"):
            inventory_api = Nginx("Inventory API")
            
            with Cluster("Domain Layer"):
                inventory_domain = Python("Inventory Domain")
            
            with Cluster("Application Layer"):
                inventory_app = Flask("Inventory Service")
            
            with Cluster("Infrastructure Layer"):
                inventory_db = MongoDB("Inventory DB")
            
            inventory_api >> inventory_app >> inventory_domain
            inventory_domain >> inventory_app >> inventory_db
    
    # Event communication between bounded contexts
    customer_app >> Edge(label="CustomerCreated") >> kafka
    kafka >> Edge(label="CustomerCreated") >> order_app
    
    order_app >> Edge(label="OrderPlaced") >> kafka
    kafka >> Edge(label="OrderPlaced") >> inventory_app
    
    inventory_app >> Edge(label="InventoryReserved") >> kafka
    kafka >> Edge(label="InventoryReserved") >> order_app