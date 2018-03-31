# Infrastructure automation

The goal of this part is to automate infrastructure deployments by using two
tools:

- **Terraform**: allows us to define infrastructure as code and easily deploy
it (by spawning machines automatically)
- **Ansible**: deploys all the software stack on a server after it has been
deployed by *Terraform*


## Terraform

All the stuff resides on `terraform` folder.

For our needs, Terraform handles Public Cloud Instances deployments on OVH
thanks to the OpenStack API and also handles DNS entry creation/deletion.

Before using it, please read the Terraform doc on their website and populate
the `terraform.tfvars` with the API credentials .

```bash
cd terraform
cp terraform.tfvars.default terraform.tfvars

# Add your credentials
vim terraform.tfvars

# Plan and apply your deployment
terraform plan
terraform apply
```
