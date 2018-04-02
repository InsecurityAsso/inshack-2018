# Infrastructure automation

The goal of this part is to automate infrastructure deployments by using these
tools:

- **Terraform**: allows us to define infrastructure as code and easily deploy
it (by spawning machines automatically)
- **Ansible**: deploys all the software stack on a server after it has been
deployed by *Terraform*
- `terraform-inventory`: a Go app that converts the *Terraform* state file into an
*Ansible* playbook


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

Please note that Terraform keeps a file named `terraform.tfstate` which is
updated after each deployment, in order to keep track of the currently deployed
machines. Thus, if you want to run a deployment from a different machine that
the one that spawned the initial infra, you have to share the
`terraform.tfstate` before. Otherwise, a new infra will be deployed!


## Ansible

Todo
