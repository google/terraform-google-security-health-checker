# terraform-google-security-health-checker

This module will deploy a cloud function that can be used by infrastructure developers or a build pipeline to detect security findings during infrastructure development.

The resources/services/activations/deletions that this module will create/trigger are:

- A Cloud function to assess the security findings during infrastructure development

## Usage

Basic usage of this module is as follows:

```hcl
module "security_health_checker" {
  source  = "terraform-google-modules/security-health-checker/google"
  version = "~> 0.1"

  project_id  = "<PROJECT ID>"
  org_id = "<Google Cloud Organization ID>"
  identity_running_function ="Google group that will have permission to invoke the cloud function"

}
```
Then perform the following commands on the root folder:

- `terraform init` to get the plugins
- `terraform plan` to see the infrastructure plan
- `terraform apply` to apply the infrastructure build
- `terraform destroy` to destroy the built infrastructure

Functional examples are included in the
[examples](./examples/) directory.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| activate\_apis | The list of apis to activate for Cloud Function | `list(string)` | <pre>[<br>  "storage.googleapis.com",<br>  "cloudfunctions.googleapis.com",<br>  "securitycenter.googleapis.com",<br>  "cloudbuild.googleapis.com"<br>]</pre> | no |
| compliance\_framework | Compliance framework to base security health check on | `string` | `"pci"` | no |
| critical\_max | Number of critical findings before alerting | `string` | `"0"` | no |
| disable\_dependent\_services | Whether services that are enabled and which depend on this service should also be disabled when this service is destroyed. https://www.terraform.io/docs/providers/google/r/google_project_service.html#disable_dependent_services | `string` | `"false"` | no |
| disable\_services\_on\_destroy | Whether project services will be disabled when the resources are destroyed. https://www.terraform.io/docs/providers/google/r/google_project_service.html#disable_on_destroy | `string` | `"false"` | no |
| enable\_apis | Whether to actually enable the APIs. If false, this module is a no-op. | `string` | `"true"` | no |
| environment | Unique environment name to link the deployment together | `string` | `"scc-health"` | no |
| function\_entry\_point | Name of function in python script | `string` | `"scc_helper_updated"` | no |
| high\_max | Number of high findings before alerting | `string` | `"10"` | no |
| identity\_running\_function | Google group that will have permission to invoke the cloud function | `string` | n/a | yes |
| medium\_max | Number of medium findings before alerting | `string` | `"20"` | no |
| org\_id | Organization ID to monitor Security Health | `any` | n/a | yes |
| project\_id | Google Cloud Project where Cloud Function will be deployed | `any` | n/a | yes |
| region | Region where cloud function is deployed | `string` | `"us-central1"` | no |
| runtime | Runtime environment for cloud function | `string` | `"python37"` | no |

## Outputs

No output.

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Requirements

These sections describe requirements for using this module.

### Software

The following dependencies must be available:

- [Terraform][terraform] v0.13
- [Terraform Provider for GCP][terraform-provider-gcp] plugin v3.0

### Service Account

A service account with the following roles must be used to provision
the resources of this module:

- Storage Admin: `roles/storage.admin`
- Cloud Function Admin: `roles/cloudfunctions.admin`
- Security Admin: `roles/iam.securityAdmin`

The [Project Factory module][project-factory-module] and the
[IAM module][iam-module] may be used in combination to provision a
service account with the necessary roles applied.

### APIs

A project with the following APIs enabled must be used to host the
resources of this module:

- Cloud Functions JSON API: `cloudfunctions.googleapis.com`
- Google Cloud Storage JSON API: `storage-api.googleapis.com`
- Security Command Center JSON API: `securitycenter.googleapis.com`

The [Project Factory module][project-factory-module] can be used to
provision a project with the necessary APIs enabled.

## Contributing

Refer to the [contribution guidelines](./CONTRIBUTING.md) for
information on contributing to this module.

[iam-module]: https://registry.terraform.io/modules/terraform-google-modules/iam/google
[project-factory-module]: https://registry.terraform.io/modules/terraform-google-modules/project-factory/google
[terraform-provider-gcp]: https://www.terraform.io/docs/providers/google/index.html
[terraform]: https://www.terraform.io/downloads.html

## Security Disclosures

Please see our [security disclosure process](./SECURITY.md).
