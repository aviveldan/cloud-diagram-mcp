"""
Terraform Plan & Architecture Visualizer
Generates hierarchical cloud architecture diagrams showing infrastructure
and its evolution via Terraform plans.
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure Graphviz is on PATH for common installation locations
_GRAPHVIZ_PATHS = [
    r"C:\Program Files\Graphviz\bin",
    r"C:\Program Files (x86)\Graphviz\bin",
]
if sys.platform == "win32":
    for _gv_path in _GRAPHVIZ_PATHS:
        if os.path.isdir(_gv_path) and _gv_path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = _gv_path + os.pathsep + os.environ.get("PATH", "")

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

# ---------------------------------------------------------------------------
# Icon mapping for Terraform resource types to Diagrams classes
# ---------------------------------------------------------------------------
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

# Map resource types to architectural layers
LAYER_MAPPING = {
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
    "azurerm_container_group": "compute",
    "azurerm_app_service": "compute",
    "azurerm_mssql_server": "database",
    "azurerm_mssql_database": "database",
    "azurerm_cosmosdb_account": "database",
    "azurerm_storage_account": "storage",
    "azurerm_storage_blob": "storage",
    "azurerm_storage_container": "storage",
    "azurerm_user_assigned_identity": "security",
    "azurerm_network_security_group": "security",
    # GCP
    "google_compute_network": "network",
    "google_compute_subnetwork": "network",
    "google_compute_forwarding_rule": "load_balancer",
    "google_compute_instance": "compute",
    "google_container_cluster": "compute",
    "google_app_engine_application": "compute",
    "google_sql_database_instance": "database",
    "google_firestore_database": "database",
    "google_storage_bucket": "storage",
}

# Edge colors for connection actions
EDGE_COLORS = {
    "create": "#4caf50",  # green — new connection
    "delete": "#f44336",  # red — removed connection
    "no-op": "gray",  # grey — unchanged
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


def _make_edge(action: str = "no-op", label: Optional[str] = None) -> Edge:
    """Create a styled Edge based on the connection action."""
    color = EDGE_COLORS.get(action, "gray")
    style = "dashed" if action == "no-op" else "bold"
    penwidth = "1.0" if action == "no-op" else "2.0"
    kwargs: Dict[str, Any] = {"color": color, "style": style, "penwidth": penwidth}
    if label:
        kwargs["label"] = label
        kwargs["fontsize"] = "9"
        kwargs["fontcolor"] = color
    return Edge(**kwargs)


def _empty_layers() -> Dict[str, List[Dict[str, Any]]]:
    return {
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


def _render_label(name: str, action: str) -> str:
    """Generate a node label with an optional action indicator."""
    symbol = {"create": "+", "delete": "-", "update": "~", "replace": "*"}.get(action, "")
    return f"[{symbol}] {name}" if symbol else name


def _place_nodes(
    resources_by_layer: Dict[str, List[Dict[str, Any]]],
    node_objects: Dict[str, Any],
) -> None:
    """Place all resource nodes into their hierarchical clusters."""

    # Layer 1: DNS & CDN
    if resources_by_layer["dns"] or resources_by_layer["cdn"]:
        with Cluster("Internet Layer"):
            if resources_by_layer["dns"]:
                with Cluster("DNS"):
                    for item in resources_by_layer["dns"]:
                        _place_one(item, node_objects)
            if resources_by_layer["cdn"]:
                with Cluster("CDN"):
                    for item in resources_by_layer["cdn"]:
                        _place_one(item, node_objects)

    # Layer 2: Network
    if resources_by_layer["network"]:
        with Cluster("Network Infrastructure"):
            vpcs = [
                r
                for r in resources_by_layer["network"]
                if "vpc" in r["type"] or "virtual_network" in r["type"]
            ]
            subnets = [r for r in resources_by_layer["network"] if "subnet" in r["type"]]
            gateways = [r for r in resources_by_layer["network"] if "gateway" in r["type"]]
            others = [
                r
                for r in resources_by_layer["network"]
                if r not in vpcs and r not in subnets and r not in gateways
            ]
            for item in vpcs:
                _place_one(item, node_objects)
            if subnets:
                pub = [r for r in subnets if "public" in r["name"]]
                priv = [r for r in subnets if "private" in r["name"]]
                other_sub = [r for r in subnets if r not in pub and r not in priv]
                if pub:
                    with Cluster("Public Subnets"):
                        for item in pub:
                            _place_one(item, node_objects)
                if priv:
                    with Cluster("Private Subnets"):
                        for item in priv:
                            _place_one(item, node_objects)
                for item in other_sub:
                    _place_one(item, node_objects)
            for item in gateways:
                _place_one(item, node_objects)
            for item in others:
                _place_one(item, node_objects)

    # Layer 3: Load Balancers
    if resources_by_layer["load_balancer"]:
        with Cluster("Load Balancing"):
            for item in resources_by_layer["load_balancer"]:
                _place_one(item, node_objects)

    # Layer 4: Compute
    if resources_by_layer["compute"]:
        with Cluster("Compute Layer"):
            az_groups: Dict[str, list] = {}
            for item in resources_by_layer["compute"]:
                name = item["name"]
                if "az1" in name or "_1" in name:
                    az = "Availability Zone 1"
                elif "az2" in name or "_2" in name:
                    az = "Availability Zone 2"
                else:
                    az = "Compute Instances"
                az_groups.setdefault(az, []).append(item)
            for az_name, items in az_groups.items():
                if len(az_groups) > 1:
                    with Cluster(az_name):
                        for item in items:
                            _place_one(item, node_objects)
                else:
                    for item in items:
                        _place_one(item, node_objects)

    # Layer 5: Data
    if resources_by_layer["database"] or resources_by_layer["cache"]:
        with Cluster("Data Layer"):
            if resources_by_layer["database"]:
                with Cluster("Database"):
                    for item in resources_by_layer["database"]:
                        _place_one(item, node_objects)
            if resources_by_layer["cache"]:
                with Cluster("Cache"):
                    for item in resources_by_layer["cache"]:
                        _place_one(item, node_objects)

    # Layer 6: Storage
    if resources_by_layer["storage"]:
        with Cluster("Storage"):
            for item in resources_by_layer["storage"]:
                _place_one(item, node_objects)

    # Layer 7: Security
    if resources_by_layer["security"]:
        with Cluster("Security & IAM"):
            for item in resources_by_layer["security"]:
                _place_one(item, node_objects)


def _place_one(item: Dict[str, Any], node_objects: Dict[str, Any]) -> None:
    """Place a single resource node in the diagram."""
    icon_class = get_icon_class(item["type"])
    label = _render_label(item["name"], item.get("action", "no-op"))
    node_objects[item["address"]] = icon_class(label, nodeid=item["address"])


def _read_svg(output_file: Path) -> str:
    """Read generated SVG and decode safely."""
    svg_path = f"{output_file}.svg"
    with open(svg_path, "rb") as f:
        raw = f.read()
    return raw.decode("utf-8", errors="ignore")


def _diagram_attrs(title: str):
    """Return common Diagram constructor kwargs."""
    tmp_dir = tempfile.mkdtemp()
    output_file = Path(tmp_dir) / "diagram"
    return (
        dict(
            name=title,
            filename=str(output_file),
            show=False,
            direction="TB",
            graph_attr={
                "fontsize": "14",
                "bgcolor": "white",
                "pad": "0.8",
                "rankdir": "TB",
                "splines": "spline",
                "nodesep": "0.8",
                "ranksep": "1.0",
            },
            node_attr={"width": "1.5", "height": "1.8", "fixedsize": "true", "fontsize": "11"},
            edge_attr={"minlen": "2"},
            outformat="svg",
        ),
        output_file,
    )


# ---------------------------------------------------------------------------
# Public API: generate SVG from Terraform plan (diff mode)
# ---------------------------------------------------------------------------


def generate_svg(plan_data: Dict[str, Any]) -> str:
    """
    Generate an SVG diagram from Terraform plan data with color-coded edges.

    Edge colors: green = new dependency, red = removed, grey = unchanged.
    """
    resource_changes = plan_data.get("resource_changes", [])
    configuration = plan_data.get("configuration", {})

    resources_by_layer = _empty_layers()

    # Build a set of resource addresses and their actions for edge coloring
    resource_actions: Dict[str, str] = {}

    for resource in resource_changes:
        action = get_primary_action(resource["change"]["actions"])
        resource_type = resource["type"]
        address = resource["address"]
        layer = LAYER_MAPPING.get(resource_type, "compute")
        resource_actions[address] = action
        resources_by_layer[layer].append(
            {
                "address": address,
                "type": resource_type,
                "name": resource["name"],
                "action": action,
            }
        )

    attrs, output_file = _diagram_attrs("Terraform Plan")
    node_objects: Dict[str, Any] = {}

    with Diagram(**attrs):
        _place_nodes(resources_by_layer, node_objects)

        # Add connections with color coding
        root_module = configuration.get("root_module", {})
        for rc in root_module.get("resources", []):
            address = rc.get("address")
            deps = rc.get("depends_on", [])
            if address not in node_objects:
                continue
            src_action = resource_actions.get(address, "no-op")
            for dep in deps:
                if dep not in node_objects:
                    continue
                dep_action = resource_actions.get(dep, "no-op")
                # Determine edge action:
                # If either endpoint is being created, the edge is new
                # If either endpoint is being deleted, the edge is removed
                # Otherwise unchanged
                if src_action == "create" or dep_action == "create":
                    edge_action = "create"
                elif src_action == "delete" or dep_action == "delete":
                    edge_action = "delete"
                else:
                    edge_action = "no-op"
                node_objects[dep] >> _make_edge(edge_action) >> node_objects[address]

    return _read_svg(output_file)


# ---------------------------------------------------------------------------
# Public API: generate SVG from architecture description (no diff)
# ---------------------------------------------------------------------------


def generate_architecture_svg(arch_data: Dict[str, Any]) -> str:
    """
    Generate an SVG diagram from an architecture description.

    Args:
        arch_data: Dict with keys:
            - title (str, optional): diagram title
            - resources: list of {address, type, name, config?}
            - connections: list of {from, to, label?, action?}
              action is "create" (green), "delete" (red), or omitted (grey)

    Returns:
        SVG content as a string
    """
    title = arch_data.get("title", "Cloud Architecture")
    resources = arch_data.get("resources", [])
    connections = arch_data.get("connections", [])

    resources_by_layer = _empty_layers()
    for res in resources:
        rtype = res.get("type", "")
        layer = LAYER_MAPPING.get(rtype, "compute")
        resources_by_layer[layer].append(
            {
                "address": res["address"],
                "type": rtype,
                "name": res.get("name", res["address"]),
                "action": "no-op",
            }
        )

    attrs, output_file = _diagram_attrs(title)
    node_objects: Dict[str, Any] = {}

    with Diagram(**attrs):
        _place_nodes(resources_by_layer, node_objects)

        for conn in connections:
            src = conn.get("from", "")
            dst = conn.get("to", "")
            if src in node_objects and dst in node_objects:
                action = conn.get("action", "no-op")
                label = conn.get("label")
                node_objects[src] >> _make_edge(action, label) >> node_objects[dst]

    return _read_svg(output_file)


# ---------------------------------------------------------------------------
# Legacy helper kept for backward compat
# ---------------------------------------------------------------------------


def get_resource_label(resource: Dict[str, Any], action: str) -> str:
    """Generate a label for a resource including action indicator."""
    return _render_label(resource["name"], action)
