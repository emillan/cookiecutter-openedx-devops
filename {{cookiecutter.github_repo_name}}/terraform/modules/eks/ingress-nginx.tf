#------------------------------------------------------------------------------
# written by: Lawrence McDaniel
#             https://lawrencemcdaniel.com
#
# date: Mar-2022
#
# usage: Add an Nginx Ingress Controller to EKS cluster
#
# see:
# - https://kubernetes.github.io/ingress-nginx/
# - https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/
# - https://registry.terraform.io/providers/hashicorp/helm/latest/docs/resources/release
#
# notes:
# 784 contributors.
# 6,300 forks
# 12,000 stars
# last commit was 16 hours ago
#------------------------------------------------------------------------------


data "kubernetes_service" "ingress_nginx_controller" {
  metadata {
    name      = "ingress-nginx-controller"
    namespace = "ingress-nginx"
  }
  depends_on = [helm_release.ingress-nginx]
}


data "aws_elb_hosted_zone_id" "main" {}


resource "helm_release" "ingress-nginx" {
  name             = "ingress-nginx"
  namespace        = "ingress-nginx"
  create_namespace = true
  disable_webhooks = false
  chart            = "ingress-nginx"
  repository       = "https://kubernetes.github.io/ingress-nginx"
  version          = "{{ cookiecutter.terraform_helm_ingress_nginx }}"

  set {
    name  = "controller.name"
    value = "nginx-controller"
  }

  # internal use only since we're behind a load balancer
  set {
    name  = "controller.service.type"
    value = "ClusterIP"
  }

  # and so, we do not need https either
  set {
    name  = "controller.service.enableHttps"
    value = false
  }

  set {
    name  = "defaultBackend.enabled"
    value = false
  }

  # mcdaniel
  # https://www.cyberciti.biz/faq/nginx-upstream-sent-too-big-header-while-reading-response-header-from-upstream/
  # to fix "[error] 199#199: *15739 upstream sent too big header while reading response header from upstream"
  # ---------------------
  set {
    name  = "ingress.annotations.nginx.ingress.kubernetes.io/proxy-busy-buffers-size"
    value = "512k"
  }

  set {
    name  = "ingress.annotations.nginx.ingress.kubernetes.io/proxy-buffers"
    value = "4 512k"
  }

  set {
    name  = "ingress.annotations.nginx.ingress.kubernetes.io/proxy-buffer-size"
    value = "256k"
  }

  depends_on = [
    module.eks
  ]
}
