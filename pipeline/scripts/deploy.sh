#!/bin/bash
set -e
echo "Deploying ${APP_NAME}:${BUILD_NUMBER}..."
docker stop ${APP_NAME} 2>/dev/null || true
docker rm   ${APP_NAME} 2>/dev/null || true
docker run -d \
  --name ${APP_NAME} \
  --restart unless-stopped \
  -p 5000:5000 \
  ${APP_NAME}:${BUILD_NUMBER}
echo "Deployment complete. App running on port 5000."
