"""
Terraform Plan Visualizer
Generates cloud architecture diagrams from Terraform plan JSON using the Diagrams library.
"""

import os
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
    """Get the appropriate Diagrams icon class for a Terraform resource type.
    
    Args:
        resource_type: The Terraform resource type (e.g., "aws_instance", "azurerm_virtual_machine")
    
    Returns:
        The Diagrams icon class to use. Defaults to EC2 for unknown types as a generic compute icon.
    """
    return ICON_MAPPING.get(resource_type, EC2)  # Default to EC2 as generic compute icon


def get_primary_action(actions: List[str]) -> str:
    """
    Determine the primary action from a list of Terraform actions.
    
    Args:
        actions: List of action strings (e.g., ["create"], ["delete"], ["create", "delete"])
    
    Returns:
        Primary action: "create", "delete", "update", "replace", or "no-op"
    """
    if "create" in actions and "delete" in actions:
        return "replace"
    if "delete" in actions:
        return "delete"
    if "create" in actions:
        return "create"
    if "update" in actions:
        return "update"
    return "no-op"


def get_action_color(action: str) -> str:
    """
    Get the color code for a specific action type.
    
    Args:
        action: Action type ("create", "delete", "update", "replace", "no-op")
    
    Returns:
        HTML color code
    """
    colors = {
        "create": "#2E7D32",  # Green
        "delete": "#C62828",  # Red
        "update": "#F57F17",  # Orange
        "replace": "#6A1B9A",  # Purple
        "no-op": "#757575",   # Gray
    }
    return colors.get(action, "#000000")


def visualize_terraform_plan(plan_data: Dict[str, Any]) -> Tuple[str, str]:
    """
    Generate a visual diagram from Terraform plan data.
    
    Args:
        plan_data: Parsed Terraform plan JSON
    
    Returns:
        Tuple of (output_file_path, summary_text)
    """
    resource_changes = plan_data.get("resource_changes", [])
    
    # Count actions
    action_counts = {
        "create": 0,
        "delete": 0,
        "update": 0,
        "replace": 0,
    }
    
    # Process resources
    resources_by_action = {
        "create": [],
        "delete": [],
        "update": [],
        "replace": [],
        "no-op": [],
    }
    
    for resource in resource_changes:
        action = get_primary_action(resource["change"]["actions"])
        if action != "no-op":
            resources_by_action[action].append(resource)
            action_counts[action] += 1
    
    # Create the diagram
    output_dir = Path.cwd() / "terraform-diffs"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "terraform_plan_diff"
    
    # Set diagram attributes for better visuals
    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.5",
    }
    
    with Diagram(
        "Terraform Plan Changes",
        filename=str(output_file),
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png",
    ):
        # Group resources by action type
        for action in ["create", "delete", "update", "replace"]:
            resources = resources_by_action[action]
            if not resources:
                continue
            
            action_label = {
                "create": "🟢 Creating",
                "delete": "🔴 Deleting",
                "update": "🟠 Updating",
                "replace": "🟣 Replacing",
            }[action]
            
            with Cluster(action_label):
                for resource in resources:
                    resource_type = resource["type"]
                    resource_name = resource["name"]
                    icon_class = get_icon_class(resource_type)
                    
                    # Create the node with the resource name
                    # The diagrams library doesn't support custom border colors directly,
                    # so we add emoji indicators and rely on cluster grouping
                    label = f"{resource_name}\n({resource_type})"
                    icon_class(label)
    
    # Generate summary
    summary_lines = []
    summary_lines.append(f"- ✨ **Create**: {action_counts['create']} resources")
    summary_lines.append(f"- 📝 **Update**: {action_counts['update']} resources")
    summary_lines.append(f"- 🗑️ **Delete**: {action_counts['delete']} resources")
    summary_lines.append(f"- 🔄 **Replace**: {action_counts['replace']} resources")
    summary_lines.append(f"\n**Total changes**: {sum(action_counts.values())} resources")
    
    summary = "\n".join(summary_lines)
    
    # Return the output file path (without extension, diagrams adds it)
    return f"{output_file}.png", summary
