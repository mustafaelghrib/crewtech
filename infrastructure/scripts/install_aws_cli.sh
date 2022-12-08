while getopts "C:S:R:A:" flag; do
  case "${flag}" in
  C) ACCESS_KEY=${OPTARG} ;;
  S) SECRET_KEY=${OPTARG} ;;
  R) REGION=${OPTARG} ;;
  A) ACCOUNT_ID=${OPTARG} ;;
  esac
done

echo "Install AWS CLI"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip -o awscliv2.zip
sudo ./aws/install
aws --version

echo "Configure AWS CLI"
aws configure set aws_access_key_id "$ACCESS_KEY"
aws configure set aws_secret_access_key "$SECRET_KEY"
aws configure set default.region "$REGION"

echo "Login to AWS ECR"
aws ecr get-login-password --region "$REGION" | docker login \
--username AWS \
--password-stdin "$ACCOUNT_ID".dkr.ecr."$REGION".amazonaws.com
