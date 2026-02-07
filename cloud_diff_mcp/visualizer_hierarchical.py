"""
Enhanced Terraform Plan Visualizer
Generates hierarchical cloud architecture diagrams showing infrastructure evolution.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple, Set

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

from cloud_diff_mcp.visualizer import ICON_MAPPING, get_icon_class, get_primary_action


def visualize_terraform_plan_hierarchical(plan_data: Dict[str, Any]) -> Tuple[str, str]:
    """
    Generate a hierarchical visual diagram from Terraform plan data.
    Shows architecture organized by layers and includes unchanged resources for context.
    
    Args:
        plan_data: Parsed Terraform plan JSON
    
    Returns:
        Tuple of (output_file_path, summary_text)
    """
    resource_changes = plan_data.get("resource_changes", [])
    
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
    
    # Create the diagram
    output_dir = Path.cwd() / "terraform-diffs"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "terraform_plan_diff_complex"
    
    # Set diagram attributes for hierarchical layout
    graph_attr = {
        "fontsize": "16",
        "bgcolor": "white",
        "pad": "0.5",
        "rankdir": "TB",
        "splines": "ortho",
    }
    
    node_objects = {}  # Store node objects for creating edges
    
    with Diagram(
        "Terraform Plan - Complex Architecture",
        filename=str(output_file),
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png",
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
    
    # Generate summary
    summary_lines = []
    summary_lines.append(f"- ✨ **Create**: {action_counts['create']} resources")
    summary_lines.append(f"- 📝 **Update**: {action_counts['update']} resources")
    summary_lines.append(f"- 🗑️ **Delete**: {action_counts['delete']} resources")
    summary_lines.append(f"- 🔄 **Replace**: {action_counts['replace']} resources")
    summary_lines.append(f"\n**Total changes**: {sum(action_counts.values())} resources")
    
    summary = "\n".join(summary_lines)
    
    return f"{output_file}.png", summary


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
