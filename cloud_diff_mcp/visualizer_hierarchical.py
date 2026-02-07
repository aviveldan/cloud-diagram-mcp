"""
Terraform Plan Visualizer
Generates hierarchical cloud architecture diagrams showing infrastructure evolution.
"""

import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import VPC, ELB, InternetGateway, NATGateway, Route53, CloudFront
from diagrams.aws.security import IAM, SecretsManager, WAF
from diagrams.aws.storage import S3, EBS, EFS
from diagrams.azure.compute import VM, ContainerInstances, AppServices
from diagrams.azure.database import SQLDatabases, CosmosDb
from diagrams.azure.identity import ManagedIdentities
from diagrams.azure.network import VirtualNetworks, LoadBalancers, ApplicationGateway, DNSZones
from diagrams.azure.storage import StorageAccounts, BlobStorage
from diagrams.gcp.compute import ComputeEngine, GKE, AppEngine
from diagrams.gcp.database import SQL, Firestore
from diagrams.gcp.network import VPC as GcpVPC, LoadBalancing
from diagrams.gcp.storage import GCS


# Icon mapping for Terraform resource types to Diagrams classes
ICON_MAPPING = {
    # AWS Resources
    "aws_instance": EC2,
    "aws_vpc": VPC,
    "aws_subnet": VPC,
    "aws_security_group": IAM,
    "aws_db_instance": RDS,
    "aws_rds_cluster": RDS,
    "aws_elasticache_cluster": ElastiCache,
    "aws_elasticache_replication_group": ElastiCache,
    "aws_s3_bucket": S3,
    "aws_ebs_volume": EBS,
    "aws_efs_file_system": EFS,
    "aws_elb": ELB,
    "aws_lb": ELB,
    "aws_alb": ELB,
    "aws_internet_gateway": InternetGateway,
    "aws_nat_gateway": NATGateway,
    "aws_route53_zone": Route53,
    "aws_route53_record": Route53,
    "aws_cloudfront_distribution": CloudFront,
    "aws_iam_role": IAM,
    "aws_iam_user": IAM,
    "aws_iam_policy": IAM,
    "aws_secretsmanager_secret": SecretsManager,
    "aws_wafv2_web_acl": WAF,
    # Azure Resources
    "azurerm_virtual_machine": VM,
    "azurerm_linux_virtual_machine": VM,
    "azurerm_windows_virtual_machine": VM,
    "azurerm_virtual_network": VirtualNetworks,
    "azurerm_subnet": VirtualNetworks,
    "azurerm_network_security_group": VirtualNetworks,
    "azurerm_mssql_server": SQLDatabases,
    "azurerm_mssql_database": SQLDatabases,
    "azurerm_cosmosdb_account": CosmosDb,
    "azurerm_storage_account": StorageAccounts,
    "azurerm_storage_blob": BlobStorage,
    "azurerm_storage_container": BlobStorage,
    "azurerm_lb": LoadBalancers,
    "azurerm_application_gateway": ApplicationGateway,
    "azurerm_dns_zone": DNSZones,
    "azurerm_user_assigned_identity": ManagedIdentities,
    "azurerm_container_group": ContainerInstances,
    "azurerm_app_service": AppServices,
    # GCP Resources
    "google_compute_instance": ComputeEngine,
    "google_compute_network": GcpVPC,
    "google_compute_subnetwork": GcpVPC,
    "google_sql_database_instance": SQL,
    "google_firestore_database": Firestore,
    "google_storage_bucket": GCS,
    "google_compute_forwarding_rule": LoadBalancing,
    "google_container_cluster": GKE,
    "google_app_engine_application": AppEngine,
}


def get_icon_class(resource_type: str) -> Any:
    """Get the Diagrams icon class for a Terraform resource type."""
    return ICON_MAPPING.get(resource_type, EC2)


def get_primary_action(actions: List[str]) -> str:
    """Determine the primary action from a list of Terraform actions."""
    if "create" in actions and "delete" in actions:
        return "replace"
    if "delete" in actions:
        return "delete"
    if "create" in actions:
        return "create"
    if "update" in actions:
        return "update"
    return "no-op"


def generate_svg(plan_data: Dict[str, Any]) -> str:
    """
    Generate an SVG diagram from Terraform plan data.
    
    Args:
        plan_data: Parsed Terraform plan JSON
    
    Returns:
        SVG content as a string
    """
    resource_changes = plan_data.get("resource_changes", [])
    configuration = plan_data.get("configuration", {})
    
    # Categorize resources by type and action
    resources_by_layer = {
        "dns": [],
        "cdn": [],
        "network": [],
        "load_balancer": [],
        "compute": [],
        "database": [],
        "cache": [],
        "storage": [],
        "security": [],
    }
    
    # Map resource types to layers
    layer_mapping = {
        "aws_route53_zone": "dns",
        "aws_route53_record": "dns",
        "aws_cloudfront_distribution": "cdn",
        "aws_vpc": "network",
        "aws_subnet": "network",
        "aws_internet_gateway": "network",
        "aws_nat_gateway": "network",
        "aws_lb": "load_balancer",
        "aws_elb": "load_balancer",
        "aws_alb": "load_balancer",
        "aws_instance": "compute",
        "aws_db_instance": "database",
        "aws_rds_cluster": "database",
        "aws_elasticache_cluster": "cache",
        "aws_elasticache_replication_group": "cache",
        "aws_s3_bucket": "storage",
        "aws_ebs_volume": "storage",
        "aws_efs_file_system": "storage",
        "aws_security_group": "security",
        "aws_iam_role": "security",
        "aws_iam_policy": "security",
        "aws_secretsmanager_secret": "security",
        "aws_wafv2_web_acl": "security",
        # Azure
        "azurerm_dns_zone": "dns",
        "azurerm_virtual_network": "network",
        "azurerm_subnet": "network",
        "azurerm_lb": "load_balancer",
        "azurerm_application_gateway": "load_balancer",
        "azurerm_virtual_machine": "compute",
        "azurerm_linux_virtual_machine": "compute",
        "azurerm_windows_virtual_machine": "compute",
        "azurerm_mssql_server": "database",
        "azurerm_cosmosdb_account": "database",
        "azurerm_storage_account": "storage",
        "azurerm_storage_blob": "storage",
        "azurerm_user_assigned_identity": "security",
        "azurerm_network_security_group": "security",
    }
    
    # Track action counts
    action_counts = {
        "create": 0,
        "delete": 0,
        "update": 0,
        "replace": 0,
    }
    
    # Organize resources
    for resource in resource_changes:
        action = get_primary_action(resource["change"]["actions"])
        if action != "no-op":
            action_counts[action] += 1
        
        resource_type = resource["type"]
        layer = layer_mapping.get(resource_type, "compute")
        
        resources_by_layer[layer].append({
            "resource": resource,
            "action": action,
        })
    
    # Create the diagram in a temp directory
    tmp_dir = tempfile.mkdtemp()
    output_file = Path(tmp_dir) / "terraform_plan"
    
    # Set diagram attributes for hierarchical layout
    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.8",
        "rankdir": "TB",
        "splines": "spline",
        "nodesep": "0.8",
        "ranksep": "1.0",
    }

    node_attr = {
        "width": "1.5",
        "height": "1.8",
        "fixedsize": "true",
        "fontsize": "11",
    }

    edge_attr = {
        "minlen": "2",
    }

    node_objects = {}  # Store node objects for creating edges

    with Diagram(
        "Terraform Plan - Complex Architecture",
        filename=str(output_file),
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
        outformat="svg",
    ):
        # Layer 1: DNS & CDN (Internet-facing)
        if resources_by_layer["dns"] or resources_by_layer["cdn"]:
            with Cluster("Internet Layer"):
                if resources_by_layer["dns"]:
                    with Cluster("DNS"):
                        for item in resources_by_layer["dns"]:
                            res = item["resource"]
                            action = item["action"]
                            icon_class = get_icon_class(res["type"])
                            label = get_resource_label(res, action)
                            node_objects[res["address"]] = icon_class(label)
                
                if resources_by_layer["cdn"]:
                    with Cluster("CDN"):
                        for item in resources_by_layer["cdn"]:
                            res = item["resource"]
                            action = item["action"]
                            icon_class = get_icon_class(res["type"])
                            label = get_resource_label(res, action)
                            node_objects[res["address"]] = icon_class(label)
        
        # Layer 2: Network Infrastructure
        if resources_by_layer["network"]:
            with Cluster("Network Infrastructure"):
                # Separate VPCs and subnets
                vpcs = [r for r in resources_by_layer["network"] if "vpc" in r["resource"]["type"]]
                subnets = [r for r in resources_by_layer["network"] if "subnet" in r["resource"]["type"]]
                gateways = [r for r in resources_by_layer["network"] if "gateway" in r["resource"]["type"]]
                
                # VPCs
                for item in vpcs:
                    res = item["resource"]
                    action = item["action"]
                    icon_class = get_icon_class(res["type"])
                    label = get_resource_label(res, action)
                    node_objects[res["address"]] = icon_class(label)
                
                # Subnets grouped by public/private
                if subnets:
                    public_subnets = [r for r in subnets if "public" in r["resource"]["name"]]
                    private_subnets = [r for r in subnets if "private" in r["resource"]["name"]]
                    
                    if public_subnets:
                        with Cluster("Public Subnets"):
                            for item in public_subnets:
                                res = item["resource"]
                                action = item["action"]
                                icon_class = get_icon_class(res["type"])
                                label = get_resource_label(res, action)
                                node_objects[res["address"]] = icon_class(label)
                    
                    if private_subnets:
                        with Cluster("Private Subnets"):
                            for item in private_subnets:
                                res = item["resource"]
                                action = item["action"]
                                icon_class = get_icon_class(res["type"])
                                label = get_resource_label(res, action)
                                node_objects[res["address"]] = icon_class(label)
                
                # Gateways
                for item in gateways:
                    res = item["resource"]
                    action = item["action"]
                    icon_class = get_icon_class(res["type"])
                    label = get_resource_label(res, action)
                    node_objects[res["address"]] = icon_class(label)
        
        # Layer 3: Load Balancers
        if resources_by_layer["load_balancer"]:
            with Cluster("Load Balancing"):
                for item in resources_by_layer["load_balancer"]:
                    res = item["resource"]
                    action = item["action"]
                    icon_class = get_icon_class(res["type"])
                    label = get_resource_label(res, action)
                    node_objects[res["address"]] = icon_class(label)
        
        # Layer 4: Compute Resources
        if resources_by_layer["compute"]:
            with Cluster("Compute Layer"):
                # Group by availability zone or name pattern
                az_groups = {}
                for item in resources_by_layer["compute"]:
                    res = item["resource"]
                    name = res["name"]
                    # Try to extract AZ from name
                    if "az1" in name or "_1" in name:
                        az = "Availability Zone 1"
                    elif "az2" in name or "_2" in name:
                        az = "Availability Zone 2"
                    else:
                        az = "Compute Instances"
                    
                    if az not in az_groups:
                        az_groups[az] = []
                    az_groups[az].append(item)
                
                for az_name, items in az_groups.items():
                    if len(az_groups) > 1:
                        with Cluster(az_name):
                            for item in items:
                                res = item["resource"]
                                action = item["action"]
                                icon_class = get_icon_class(res["type"])
                                label = get_resource_label(res, action)
                                node_objects[res["address"]] = icon_class(label)
                    else:
                        for item in items:
                            res = item["resource"]
                            action = item["action"]
                            icon_class = get_icon_class(res["type"])
                            label = get_resource_label(res, action)
                            node_objects[res["address"]] = icon_class(label)
        
        # Layer 5: Data Layer (Database & Cache)
        if resources_by_layer["database"] or resources_by_layer["cache"]:
            with Cluster("Data Layer"):
                if resources_by_layer["database"]:
                    with Cluster("Database"):
                        for item in resources_by_layer["database"]:
                            res = item["resource"]
                            action = item["action"]
                            icon_class = get_icon_class(res["type"])
                            label = get_resource_label(res, action)
                            node_objects[res["address"]] = icon_class(label)
                
                if resources_by_layer["cache"]:
                    with Cluster("Cache"):
                        for item in resources_by_layer["cache"]:
                            res = item["resource"]
                            action = item["action"]
                            icon_class = get_icon_class(res["type"])
                            label = get_resource_label(res, action)
                            node_objects[res["address"]] = icon_class(label)
        
        # Layer 6: Storage
        if resources_by_layer["storage"]:
            with Cluster("Storage"):
                for item in resources_by_layer["storage"]:
                    res = item["resource"]
                    action = item["action"]
                    icon_class = get_icon_class(res["type"])
                    label = get_resource_label(res, action)
                    node_objects[res["address"]] = icon_class(label)
        
        # Layer 7: Security & IAM
        if resources_by_layer["security"]:
            with Cluster("Security & IAM"):
                for item in resources_by_layer["security"]:
                    res = item["resource"]
                    action = item["action"]
                    icon_class = get_icon_class(res["type"])
                    label = get_resource_label(res, action)
                    node_objects[res["address"]] = icon_class(label)
        
        # Add connections based on dependencies
        root_module = configuration.get("root_module", {})
        resources_config = root_module.get("resources", [])
        
        for resource_config in resources_config:
            address = resource_config.get("address")
            depends_on = resource_config.get("depends_on", [])
            
            if address in node_objects:
                for dependency in depends_on:
                    if dependency in node_objects:
                        node_objects[dependency] >> Edge(color="gray", style="dashed") >> node_objects[address]
    
    # Read and return the generated SVG content
    svg_path = f"{output_file}.svg"
    with open(svg_path, 'rb') as f:
        raw = f.read()
    # Graphviz on Windows can emit invalid UTF-8; decode leniently
    return raw.decode('utf-8', errors='replace')


def get_resource_label(resource: Dict[str, Any], action: str) -> str:
    """Generate a label for a resource including action indicator."""
    name = resource["name"]
    resource_type = resource["type"].split("_", 1)[1] if "_" in resource["type"] else resource["type"]
    
    # Action emoji
    action_emoji = {
        "create": "✨",
        "delete": "🗑️",
        "update": "📝",
        "replace": "🔄",
        "no-op": "",
    }.get(action, "")
    
    if action == "no-op":
        # Unchanged resources shown without emoji
        return f"{name}"
    else:
        return f"{action_emoji} {name}"
