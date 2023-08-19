resource "kubernetes_namespace" "hello" {
  metadata {
    name = "hello-namespace-v3"
  }
}

resource "kubernetes_deployment" "hello" {
  metadata {
    name      = "hello-deployment"
    namespace = kubernetes_namespace.hello.metadata[0].name
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "hello"
      }
    }

    template {
      metadata {
        labels = {
          app = "hello"
        }
      }

      spec {
        container {
          image             = "danielkodev/my-image:latest" # Updated image reference
          name              = "hello"
          image_pull_policy = "Always"                      # Updated pull policy
          port {
            container_port = 5000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "hello" {
  metadata {
    name      = "hello-service"
    namespace = kubernetes_namespace.hello.metadata[0].name
  }

  spec {
    selector = {
      app = kubernetes_deployment.hello.spec[0].template[0].metadata[0].labels.app
    }

    port {
      port        = 80
      target_port = 5000
    }

    type = "NodePort"
  }
}

resource "kubernetes_ingress_v1" "hello" {
  metadata {
    name      = "hello-ingress"
    namespace = kubernetes_namespace.hello.metadata[0].name
    annotations = {
      "kubernetes.io/ingress.class"           = "nginx" # Using nginx ingress controller as an example
      "nginx.ingress.kubernetes.io/rewrite-target" = "/"
    }
  }
  spec {
    rule {
      http {
        path {
          path     = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.hello.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}

