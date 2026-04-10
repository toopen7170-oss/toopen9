#!/bin/bash
git add .
current_time=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "무료 빌드 요청: $current_time"
git push origin main
echo "------------------------------------------"
echo "전송 완료! 깃허브 Actions에서 무료 빌드가 진행됩니다."
echo "------------------------------------------"
