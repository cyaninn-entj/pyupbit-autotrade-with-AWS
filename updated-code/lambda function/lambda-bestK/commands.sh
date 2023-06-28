# ECR 토큰 인증
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 501587125031.dkr.ecr.ap-northeast-2.amazonaws.com

# build
docker build -t dev_bestk:2 .

# tagging
docker tag dev_bestk:2 501587125031.dkr.ecr.ap-northeast-2.amazonaws.com/dev_bestk:2

# push
docker push 501587125031.dkr.ecr.ap-northeast-2.amazonaws.com/dev_bestk:2

