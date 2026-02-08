import React from "react";

import {
  AwsVpc, AwsSubnet, AwsInstance, AwsSecurityGroup, AwsDbInstance,
  AwsRdsCluster, AwsS3Bucket, AwsLambdaFunction, AwsElb, AwsIamRole,
  AwsRoute53Record, AwsCloudfront, AwsDynamodb, AwsSqs, AwsSns,
  AwsEcs, AwsInternetGateway, AwsNatGateway, AwsEbs, AwsSecretsManager,
} from "./aws";

import {
  AzureResourceGroup, AzureVirtualNetwork, AzureSubnet, AzureVm,
  AzureLinuxVm, AzureStorageAccount, AzureStorageBlob, AzureAppService,
  AzureFunctionApp, AzureSqlServer, AzureCosmosDb, AzureNsg, AzureLb,
  AzureAppGateway,
} from "./azure";

import {
  GcpComputeInstance, GcpComputeNetwork, GcpSubnetwork, GcpStorageBucket,
  GcpSqlInstance, GcpFirestore, GcpForwardingRule, GcpGke,
} from "./gcp";

/* Fallback icon for unknown resource types */
const DefaultIcon: React.FC = () => (
  <svg viewBox="0 0 80 80">
    <rect x="2" y="2" width="76" height="76" rx="5" fill="#222230"/>
    <rect x="18" y="18" width="44" height="44" rx="6" fill="none" stroke="#666" strokeWidth="2"/>
    <circle cx="40" cy="34" r="7" fill="#666" opacity=".2" stroke="#666" strokeWidth="1.5"/>
    <rect x="28" y="48" width="24" height="6" rx="3" fill="#666" opacity=".2"/>
  </svg>
);

/** Map Terraform resource type → React icon component */
const ICON_MAP: Record<string, React.FC> = {
  // AWS
  aws_vpc: AwsVpc,
  aws_subnet: AwsSubnet,
  aws_instance: AwsInstance,
  aws_security_group: AwsSecurityGroup,
  aws_db_instance: AwsDbInstance,
  aws_rds_cluster: AwsRdsCluster,
  aws_s3_bucket: AwsS3Bucket,
  aws_lambda_function: AwsLambdaFunction,
  aws_elb: AwsElb,
  aws_lb: AwsElb,
  aws_alb: AwsElb,
  aws_iam_role: AwsIamRole,
  aws_iam_user: AwsIamRole,
  aws_iam_policy: AwsIamRole,
  aws_route53_zone: AwsRoute53Record,
  aws_route53_record: AwsRoute53Record,
  aws_cloudfront_distribution: AwsCloudfront,
  aws_dynamodb_table: AwsDynamodb,
  aws_sqs_queue: AwsSqs,
  aws_sns_topic: AwsSns,
  aws_ecs_cluster: AwsEcs,
  aws_ecs_service: AwsEcs,
  aws_internet_gateway: AwsInternetGateway,
  aws_nat_gateway: AwsNatGateway,
  aws_ebs_volume: AwsEbs,
  aws_efs_file_system: AwsEbs,
  aws_secretsmanager_secret: AwsSecretsManager,
  aws_wafv2_web_acl: AwsSecurityGroup,
  aws_elasticache_cluster: AwsDbInstance,
  aws_elasticache_replication_group: AwsDbInstance,
  // Azure
  azurerm_resource_group: AzureResourceGroup,
  azurerm_virtual_network: AzureVirtualNetwork,
  azurerm_subnet: AzureSubnet,
  azurerm_virtual_machine: AzureVm,
  azurerm_linux_virtual_machine: AzureLinuxVm,
  azurerm_windows_virtual_machine: AzureVm,
  azurerm_storage_account: AzureStorageAccount,
  azurerm_storage_blob: AzureStorageBlob,
  azurerm_storage_container: AzureStorageBlob,
  azurerm_app_service: AzureAppService,
  azurerm_function_app: AzureFunctionApp,
  azurerm_mssql_server: AzureSqlServer,
  azurerm_mssql_database: AzureSqlServer,
  azurerm_cosmosdb_account: AzureCosmosDb,
  azurerm_network_security_group: AzureNsg,
  azurerm_lb: AzureLb,
  azurerm_application_gateway: AzureAppGateway,
  azurerm_container_group: AzureAppService,
  azurerm_user_assigned_identity: AzureNsg,
  azurerm_dns_zone: AzureVirtualNetwork,
  // GCP
  google_compute_instance: GcpComputeInstance,
  google_compute_network: GcpComputeNetwork,
  google_compute_subnetwork: GcpSubnetwork,
  google_storage_bucket: GcpStorageBucket,
  google_sql_database_instance: GcpSqlInstance,
  google_firestore_database: GcpFirestore,
  google_compute_forwarding_rule: GcpForwardingRule,
  google_container_cluster: GcpGke,
  google_app_engine_application: GcpComputeInstance,
};

export function getIcon(resourceType: string): React.FC {
  return ICON_MAP[resourceType] || DefaultIcon;
}

/* Category grouping for layout */
const CATEGORIES: Record<string, { label: string; types: string[] }> = {
  networking: {
    label: "Networking",
    types: ["vpc", "subnet", "virtual_network", "network_security_group", "security_group", "internet_gateway", "nat_gateway", "route53", "cloudfront", "elb", "lb", "alb", "compute_network", "compute_subnetwork", "load_balancer", "application_gateway", "dns_zone", "forwarding_rule"],
  },
  compute: {
    label: "Compute",
    types: ["instance", "virtual_machine", "linux_virtual_machine", "windows_virtual_machine", "lambda_function", "ecs_cluster", "ecs_service", "app_service", "function_app", "compute_instance", "container_group", "container_cluster", "gke", "app_engine"],
  },
  database: {
    label: "Database",
    types: ["db_instance", "rds_cluster", "dynamodb_table", "elasticache", "sql_database", "cosmosdb", "mssql", "sql_database_instance", "firestore"],
  },
  storage: {
    label: "Storage",
    types: ["s3_bucket", "ebs_volume", "efs", "storage_account", "storage_blob", "storage_container", "storage_bucket", "gcs"],
  },
  security: {
    label: "Security & Identity",
    types: ["iam_role", "iam_user", "iam_policy", "secretsmanager", "waf", "managed_identity", "user_assigned_identity"],
  },
  messaging: {
    label: "Messaging",
    types: ["sqs_queue", "sns_topic", "kinesis"],
  },
};

export function categorize(resourceType: string): string {
  const lower = resourceType.toLowerCase();
  for (const [cat, info] of Object.entries(CATEGORIES)) {
    if (info.types.some((t) => lower.includes(t))) return cat;
  }
  return "other";
}

export function getCategoryLabel(cat: string): string {
  return CATEGORIES[cat]?.label || "Resources";
}

export function providerOf(resourceType: string): string {
  if (resourceType.startsWith("aws_")) return "aws";
  if (resourceType.startsWith("azurerm_")) return "azurerm";
  if (resourceType.startsWith("google_")) return "google";
  return "other";
}
