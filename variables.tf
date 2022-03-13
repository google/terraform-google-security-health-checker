/**
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

variable "project_id" {
  description = "Google Cloud Project where Cloud Function will be deployed"
}

variable "org_id" {
  description = "Organization ID to monitor Security Health"
}

variable "region" {
  description = "Region where cloud function is deployed"
  type        = string
  default     = "us-central1"
}

variable "enable_apis" {
  description = "Whether to actually enable the APIs. If false, this module is a no-op."
  default     = "true"
}

variable "disable_services_on_destroy" {
  description = "Whether project services will be disabled when the resources are destroyed. https://www.terraform.io/docs/providers/google/r/google_project_service.html#disable_on_destroy"
  default     = "false"
  type        = string
}

variable "disable_dependent_services" {
  description = "Whether services that are enabled and which depend on this service should also be disabled when this service is destroyed. https://www.terraform.io/docs/providers/google/r/google_project_service.html#disable_dependent_services"
  default     = "false"
  type        = string
}

variable "activate_apis" {
  description = "The list of apis to activate for Cloud Function"
  default     = ["storage.googleapis.com", "cloudfunctions.googleapis.com", "securitycenter.googleapis.com", "cloudbuild.googleapis.com"]
  type        = list(string)
}

variable "environment" {
  description = "Unique environment name to link the deployment together"
  default     = "scc-health"
}

variable "function_entry_point" {
  description = "Name of function in python script"
  default     = "scc_helper_updated"
}

variable "runtime" {
  description = "Runtime environment for cloud function"
  type        = string
  default     = "python37"
}

variable "compliance_framework" {
  description = "Compliance framework to base security health check on"
  default     = "pci"
}

variable "critical_max" {
  description = "Number of critical findings before alerting"
  default     = "0"
}

variable "high_max" {
  description = "Number of high findings before alerting"
  default     = "10"
}

variable "medium_max" {
  description = "Number of medium findings before alerting"
  default     = "20"
}

variable "identity_running_function" {
  description = "Google group that will have permission to invoke the cloud function"
  type        = string
}
