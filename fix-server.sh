#!/bin/bash
set -e

echo "=== 0. Correction des permissions sur le serveur ==="
ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa ubuntu@13.38.79.22 "sudo chown -R ubuntu:ubuntu /opt/topgainers"

echo "=== 1. Copie des fichiers de configuration ==="
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa docker-compose.yml ubuntu@13.38.79.22:/opt/topgainers/docker-compose.yml
scp -o StrictHostKeyChecking=no -r -i ~/.ssh/id_rsa grafana ubuntu@13.38.79.22:/opt/topgainers/
scp -o StrictHostKeyChecking=no -r -i ~/.ssh/id_rsa prometheus ubuntu@13.38.79.22:/opt/topgainers/

echo "=== 2. Démarrage des services ==="
ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa ubuntu@13.38.79.22 "cd /opt/topgainers && sudo docker compose up -d db && sleep 10 && sudo docker compose up -d prometheus grafana && sleep 10 && sudo docker compose up -d --build top-gainers-crypto && echo '=== ÉTAT DES CONTENEURS ===' && sudo docker compose ps"

echo "=== 3. Vérification des services ==="
echo "App (8501): $(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 10 http://13.38.79.22:8501 2>&1)"
echo "Prometheus (9090): $(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 10 http://13.38.79.22:9090/-/healthy 2>&1)"
echo "Grafana (3000): $(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 10 http://13.38.79.22:3000/api/health 2>&1)"
echo "Metrics (8000): $(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 10 http://13.38.79.22:8000/metrics 2>&1)"