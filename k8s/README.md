# Manifests Kubernetes (k3s)

Ce dossier contient les manifests Kubernetes pour déployer l'application TopGainersCrypto et sa base de données PostgreSQL sur un cluster k3s.

## Ressources

| Fichier | Description |
|---------|-------------|
| `namespace.yaml` | Namespace `topgainers` |
| `postgres-secret.yaml` | Secret contenant les identifiants PostgreSQL |
| `postgres-pvc.yaml` | Volume persistant pour PostgreSQL (10 Go) |
| `postgres-deployment.yaml` | Déploiement PostgreSQL 16 |
| `postgres-service.yaml` | Service interne PostgreSQL (ClusterIP) |
| `app-deployment.yaml` | Déploiement de l'application Streamlit |
| `app-service.yaml` | Service NodePort exposant l'application (30001) et les métriques (30002) |

## Déploiement

```bash
kubectl apply -f namespace.yaml
kubectl apply -f postgres-secret.yaml
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f app-deployment.yaml
kubectl apply -f app-service.yaml
```

Ou en une seule commande :
```bash
kubectl apply -f k8s/
```

## Vérification

```bash
kubectl get pods -n topgainers
kubectl get svc -n topgainers
```

## Accès

- **Application** : `http://<IP_VM>:30001`
- **Métriques Prometheus** : `http://<IP_VM>:30002/metrics`

## Notes

- **PostgreSQL** est exposé uniquement en interne (ClusterIP) — pas accessible depuis l'extérieur
- **L'application** est exposée via NodePort (30001 pour Streamlit, 30002 pour les métriques)
- Le mot de passe PostgreSQL est dans le Secret `postgres-secret` (à changer en production)