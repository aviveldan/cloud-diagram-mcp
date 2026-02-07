/**
 * Types for Terraform plan JSON structure
 */

export interface TerraformPlan {
  format_version?: string;
  terraform_version?: string;
  resource_changes?: ResourceChange[];
  configuration?: Configuration;
}

export interface ResourceChange {
  address: string;
  mode?: string;
  type: string;
  name: string;
  provider_name?: string;
  change: Change;
}

export interface Change {
  actions: string[];
  before?: any;
  after?: any;
  after_unknown?: any;
}

export interface Configuration {
  root_module?: Module;
}

export interface Module {
  resources?: Resource[];
}

export interface Resource {
  address: string;
  mode?: string;
  type: string;
  name: string;
  depends_on?: string[];
}
