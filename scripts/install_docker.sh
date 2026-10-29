#!/usr/bin/env bash
# EC2(Ubuntu)에 Docker를 설치합니다. 7교시 실습에서 한 번 실행합니다.
#   bash scripts/install_docker.sh
set -e
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
echo ""
echo "설치 완료. 아래 명령으로 권한을 반영한 뒤 docker --version 으로 확인하세요."
echo "  newgrp docker"
