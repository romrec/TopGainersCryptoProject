# Infrastructure Terraform AWS

Ce dossier contient la configuration Terraform pour déployer l'infrastructure TopGainersCrypto sur **Amazon Web Services (AWS)** en utilisant uniquement les ressources **Free Tier**.

## Ressources créées

| Ressource | Description |
|-----------|-------------|
| **VPC** | Réseau virtuel `10.0.0.0/16` |
| **Subnet public** | Sous-réseau `10.0.1.0/24` |
| **Internet Gateway** | Accès internet pour la VM |
| **Route Table** | Routage du trafic vers l'Internet Gateway |
| **Security Group** | Règles de pare-feu (SSH restreint, ports app/monitoring) |
| **Key Pair** | Clé SSH pour accéder à la VM |
| **Instance EC2** | `t2.micro` (1 vCPU / 1 Go RAM) — Free Tier |

## Prérequis

1. **Compte AWS** avec accès Free Tier
2. **AWS CLI** configuré avec le profil `topgainers` :
```bash
aws configure --profile topgainers
```
3. **Clé SSH** pour accéder à la VM
4. **Terraform** installé (v1.0+)

## Configuration

1. Remplir `terraform.tfvars` avec vos valeurs :
- `region` : Région AWS (ex: `eu-west-3`)
- `my_ip` : Votre IP publique (pour SSH)
- `ssh_public_key_path` : Chemin vers votre clé SSH publique

## Déploiement

```bash
# Initialiser avec le profil AWS topgainers
AWS_PROFILE=topgainers terraform init

# Vérifier le plan
AWS_PROFILE=topgainers terraform plan

# Déployer
AWS_PROFILE=topgainers terraform apply -auto-approve
```

## Sorties

Après le déploiement, Terraform affiche :
- `instance_public_ip` : IP publique de la VM
- `app_url` : URL de l'application Streamlit
- `prometheus_url` : URL de Prometheus
- `grafana_url` : URL de Grafana

## Accès

- **SSH** : `ssh -i ~/.ssh/id_rsa ubuntu@<IP_PUBLIQUE>`
- **Application** : `http://<IP_PUBLIQUE>:8501`
- **Prometheus** : `http://<IP_PUBLIQUE>:9090`
- **Grafana** : `http://<IP_PUBLIQUE>:3000`

## Sécurité

- SSH restreint à votre IP uniquement (`var.my_ip`)
- Ports applicatifs ouverts (8501, 9090, 3000)
- Pas de mot de passe, uniquement clé SSH