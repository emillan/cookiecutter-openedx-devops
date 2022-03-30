"""
"""

import os
import shutil


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def remove_clb_files():
    component_dir_path = os.path.join("terraform", "modules", "eks_ingress_clb_controller")
    if os.path.exists(component_dir_path):
        shutil.rmtree(component_dir_path)

    terragrunt_dir_path = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_ingress_clb_controller")
    if os.path.exists(terragrunt_dir_path):
        shutil.rmtree(terragrunt_dir_path)

    ci_dir_path = os.path.join("ci", "tutor-deploy", "environments", "{{ cookiecutter.environment_name }}", "k8s", "eks_clb")
    if os.path.exists(ci_dir_path):
        shutil.rmtree(ci_dir_path)

def remove_alb_files():
    component_dir_path = os.path.join("terraform", "modules", "eks_ingress_alb_controller")
    if os.path.exists(component_dir_path):
        shutil.rmtree(component_dir_path)

    terragrunt_dir_path = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_ingress_alb_controller")
    if os.path.exists(terragrunt_dir_path):
        shutil.rmtree(terragrunt_dir_path)

    ci_dir_path = os.path.join("ci", "tutor-deploy", "environments", "{{ cookiecutter.environment_name }}", "k8s", "eks_alb")
    if os.path.exists(ci_dir_path):
        shutil.rmtree(ci_dir_path)

def remove_ec2_files():
    component_dir_path = os.path.join("terraform", "modules", "eks_ec2")
    if os.path.exists(component_dir_path):
        shutil.rmtree(component_dir_path)

    terragrunt_dir_path = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_ec2")
    if os.path.exists(terragrunt_dir_path):
        shutil.rmtree(terragrunt_dir_path)

    terragrunt_alb_dir_path = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_ingress_alb_controller", "terragrunt_ec2.hcl")
    if os.path.exists(terragrunt_alb_dir_path):
        os.remove(terragrunt_alb_dir_path)

    # rename the fargate version to terragrunt.hcl
    terragrunt_alb_dir_old_name = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_ingress_alb_controller", "terragrunt_fargate.hcl")
    terragrunt_alb_dir_new_name = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_ingress_alb_controller", "terragrunt.hcl")
    if os.path.exists(terragrunt_alb_dir_old_name):
        os.rename(terragrunt_alb_dir_old_name, terragrunt_alb_dir_new_name)

def remove_fargate_files():
    component_dir_path = os.path.join("terraform", "modules", "eks_fargate")
    if os.path.exists(component_dir_path):
        shutil.rmtree(component_dir_path)

    terragrunt_dir_path = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_fargate")
    if os.path.exists(terragrunt_dir_path):
        shutil.rmtree(terragrunt_dir_path)

    terragrunt_alb_dir_path = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_ingress_alb_controller", "terragrunt_fargate.hcl")
    if os.path.exists(terragrunt_alb_dir_path):
        os.remove(terragrunt_alb_dir_path)

    # rename the ec2 version to terragrunt.hcl
    terragrunt_alb_dir_old_name = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_ingress_alb_controller", "terragrunt_ec2.hcl")
    terragrunt_alb_dir_new_name = os.path.join("terraform", "environments", "{{ cookiecutter.environment_name }}", "eks_ingress_alb_controller", "terragrunt.hcl")
    if os.path.exists(terragrunt_alb_dir_old_name):
        os.rename(terragrunt_alb_dir_old_name, terragrunt_alb_dir_new_name)

# move kubernetes manifests into the k8s folder and remove the original source folder.
def move_manifests(folder = ""):
    source = os.path.join("ci", "tutor-deploy", "environments", "{{ cookiecutter.environment_name }}", "k8s", folder)
    destination = os.path.join("ci", "tutor-deploy", "environments", "{{ cookiecutter.environment_name }}", "k8s")
    src_files = os.listdir(source)
    for file_name in src_files:
        full_file_name = os.path.join(source, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, destination)
    shutil.rmtree(source)

def main():
    compute_type = "{{ cookiecutter.eks_cluster_compute_type }}".upper()

    if "{{ cookiecutter.eks_cluster_load_balancer_type }}" == "CLB":
        remove_alb_files()
        move_manifests("eks_clb")

    if "{{ cookiecutter.eks_cluster_load_balancer_type }}" == "ALB":
        remove_clb_files()
        move_manifests("eks_alb")

    if (compute_type == "EC2"):
        remove_fargate_files()

    if (compute_type == "FARGATE"):
        remove_ec2_files()

    print(SUCCESS + "Your Open edX devops repo has been initialized." + TERMINATOR)


if __name__ == "__main__":
    main()
