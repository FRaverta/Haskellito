#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

STACK_NAME="${STACK_NAME:-haskellito-prod}"
AWS_REGION="${AWS_REGION:-us-east-1}"
SITE_NAME="${SITE_NAME:-haskellito}"
DOMAIN_NAME="${DOMAIN_NAME:-}"
CERTIFICATE_ARN="${CERTIFICATE_ARN:-}"
HOSTED_ZONE_ID="${HOSTED_ZONE_ID:-}"
PRICE_CLASS="${PRICE_CLASS:-PriceClass_100}"
SAM_ARTIFACTS_BUCKET="${SAM_ARTIFACTS_BUCKET:-}"
PLAYGROUND_IMAGE_REPOSITORY="${PLAYGROUND_IMAGE_REPOSITORY:-}"
LAMBDA_TIMEOUT_SECONDS="${LAMBDA_TIMEOUT_SECONDS:-30}"
WORKER_ACQUIRE_TIMEOUT_SECONDS="${WORKER_ACQUIRE_TIMEOUT_SECONDS:-10}"
GHCI_STARTUP_TIMEOUT_SECONDS="${GHCI_STARTUP_TIMEOUT_SECONDS:-30}"
EVAL_CMD_TIMEOUT_SECONDS="${EVAL_CMD_TIMEOUT_SECONDS:-10}"
HISTORY_CMD_TIMEOUT_SECONDS="${HISTORY_CMD_TIMEOUT_SECONDS:-5}"

PROFILE_ARGS=()
if [[ -n "${AWS_PROFILE:-}" ]]; then
  PROFILE_ARGS=(--profile "$AWS_PROFILE")
fi

PARAMETER_OVERRIDES=(
  "SiteName=${SITE_NAME}"
  "PriceClass=${PRICE_CLASS}"
  "LambdaTimeoutSeconds=${LAMBDA_TIMEOUT_SECONDS}"
  "WorkerAcquireTimeoutSeconds=${WORKER_ACQUIRE_TIMEOUT_SECONDS}"
  "GhciStartupTimeoutSeconds=${GHCI_STARTUP_TIMEOUT_SECONDS}"
  "EvalCommandTimeoutSeconds=${EVAL_CMD_TIMEOUT_SECONDS}"
  "HistoryCommandTimeoutSeconds=${HISTORY_CMD_TIMEOUT_SECONDS}"
)

if [[ -n "$DOMAIN_NAME" ]]; then
  PARAMETER_OVERRIDES+=("DomainName=${DOMAIN_NAME}")
fi

if [[ -n "$CERTIFICATE_ARN" ]]; then
  PARAMETER_OVERRIDES+=("CertificateArn=${CERTIFICATE_ARN}")
fi

if [[ -n "$HOSTED_ZONE_ID" ]]; then
  PARAMETER_OVERRIDES+=("HostedZoneId=${HOSTED_ZONE_ID}")
fi

stack_output() {
  local key="$1"
  aws cloudformation describe-stacks \
    "${PROFILE_ARGS[@]}" \
    --region "$AWS_REGION" \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='${key}'].OutputValue | [0]" \
    --output text
}

sam build -t serverless/template.yaml

SAM_DEPLOY_ARGS=(
  deploy
  "${PROFILE_ARGS[@]}" \
  -t .aws-sam/build/template.yaml \
  --stack-name "$STACK_NAME" \
  --region "$AWS_REGION" \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset \
)

if [[ -n "$SAM_ARTIFACTS_BUCKET" ]]; then
  SAM_DEPLOY_ARGS+=(--s3-bucket "$SAM_ARTIFACTS_BUCKET")
fi

if [[ -n "$PLAYGROUND_IMAGE_REPOSITORY" ]]; then
  SAM_DEPLOY_ARGS+=(
    --image-repositories "PlaygroundFunction=${PLAYGROUND_IMAGE_REPOSITORY}"
  )
else
  SAM_DEPLOY_ARGS+=(--resolve-image-repos)
fi

SAM_DEPLOY_ARGS+=(--parameter-overrides "${PARAMETER_OVERRIDES[@]}")

sam "${SAM_DEPLOY_ARGS[@]}"

cd frontend
npm ci
npm run build
cd "$ROOT"

python3 serverless/frontend/export_challenges.py

SITE_BUCKET="$(stack_output SiteBucketName)"
DISTRIBUTION_ID="$(stack_output SiteDistributionId)"
SITE_URL="$(stack_output SiteUrl)"

aws s3 sync frontend/dist "s3://${SITE_BUCKET}" \
  "${PROFILE_ARGS[@]}" \
  --region "$AWS_REGION" \
  --delete \
  --exclude "assets/*" \
  --cache-control "public,max-age=0,must-revalidate"

if [[ -d frontend/dist/assets ]]; then
  aws s3 sync frontend/dist/assets "s3://${SITE_BUCKET}/assets" \
    "${PROFILE_ARGS[@]}" \
    --region "$AWS_REGION" \
    --delete \
    --cache-control "public,max-age=31536000,immutable"
fi

aws s3 sync serverless/frontend/public/api "s3://${SITE_BUCKET}/api" \
  "${PROFILE_ARGS[@]}" \
  --region "$AWS_REGION" \
  --delete \
  --content-type application/json \
  --cache-control "public,max-age=300"

aws cloudfront create-invalidation \
  "${PROFILE_ARGS[@]}" \
  --distribution-id "$DISTRIBUTION_ID" \
  --paths "/*" \
  >/dev/null

printf 'Deployed %s\n' "$SITE_URL"
printf 'CloudFront distribution: %s\n' "$DISTRIBUTION_ID"
printf 'S3 bucket: %s\n' "$SITE_BUCKET"
