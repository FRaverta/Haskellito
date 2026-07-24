# Haskellito Serverless

This directory contains the first serverless deployment path for Haskellito.
It uses AWS SAM to package the existing FastAPI backend as a Lambda container
image with Mangum.

## Shape

```text
CloudFront
  /api/v2/playground/challenges/*/submit -> API Gateway HTTP API -> Playground Lambda
  /api/v2/playground/challenges*         -> S3 static challenge JSON
  /api/*                                 -> API Gateway HTTP API -> Playground Lambda
  /assets/*                              -> S3 static frontend assets
  /*                                     -> S3 static frontend SPA
```

The Lambda image imports the existing `backend/main.py` FastAPI app. This keeps
the initial migration small and lets the current routes continue to work while
the frontend/static challenge routing is moved behind CloudFront.

## Files

```text
serverless/
  template.yaml
  deploy_prod.sh
  frontend/
    export_challenges.py
    public/                 # generated, not committed
  lambdas/playground/
    Dockerfile
    handler.py
    requirements.txt
```

The existing `frontend/` and `backend/` directories are treated as source
inputs. Serverless-specific frontend artifacts are generated under
`serverless/frontend/public`.

## Build

From the repository root:

```sh
sam build -t serverless/template.yaml
```

## Local Invoke

After building, use SAM's generated template. For image functions, the source
template does not contain the local `ImageUri`; `.aws-sam/build/template.yaml`
does.

```sh
sam local start-api -t .aws-sam/build/template.yaml
```

Then call the API through SAM's local gateway:

```sh
curl http://127.0.0.1:3000/api/v2/playground/challenges
```

For a closer local match to the final CloudFront/S3/Lambda split, use the local
edge server documented in `serverless/frontend/README.md`.

## Deploy

The template creates:

- S3 bucket for frontend/challenge files
- CloudFront distribution
- CloudFront Origin Access Control for private S3 access
- CloudFront Function for challenge JSON rewrites
- API Gateway HTTP API and Lambda image function
- Optional Route 53 A/AAAA aliases when `HostedZoneId` is provided

For a no-custom-domain deploy:

```sh
STACK_NAME=haskellito-prod \
AWS_REGION=us-east-1 \
AWS_PROFILE=haskellito-serverless \
./serverless/deploy_prod.sh
```

If the deploy user cannot use SAM-managed artifact resources, create the SAM
artifact bucket and Lambda image repository once:

```sh
aws s3 mb s3://haskellito-sam-artifacts-<account-id>-us-east-1 \
  --region us-east-1 \
  --profile haskellito-serverless

aws ecr create-repository \
  --repository-name haskellito/playground \
  --region us-east-1 \
  --profile haskellito-serverless
```

Then pass them to the repeatable deploy:

```sh
STACK_NAME=haskellito-prod \
AWS_REGION=us-east-1 \
AWS_PROFILE=haskellito-serverless \
SAM_ARTIFACTS_BUCKET=haskellito-sam-artifacts-<account-id>-us-east-1 \
PLAYGROUND_IMAGE_REPOSITORY=<account-id>.dkr.ecr.us-east-1.amazonaws.com/haskellito/playground \
./serverless/deploy_prod.sh
```

`SAM_ARTIFACTS_BUCKET` maps to `sam deploy --s3-bucket`. The website bucket is
still created by the stack and is different from this packaging bucket.
`PLAYGROUND_IMAGE_REPOSITORY` maps to `sam deploy --image-repositories`, which
avoids SAM's managed image-repository companion stack.

For a custom domain deploy, create or reuse an ACM certificate in `us-east-1`
for the domain, then pass the parameters:

```sh
STACK_NAME=haskellito-prod \
AWS_REGION=us-east-1 \
AWS_PROFILE=haskellito-serverless \
SITE_NAME=haskellito \
DOMAIN_NAME=haskellito.com \
CERTIFICATE_ARN=arn:aws:acm:us-east-1:123456789012:certificate/example \
HOSTED_ZONE_ID=Z1234567890ABC \
./serverless/deploy_prod.sh
```

Omit `HOSTED_ZONE_ID` if Route 53 should not be managed by this stack.

The script runs `sam build`, `sam deploy`, builds the Vue app, exports public
challenge JSON, syncs static files to the stack-created S3 bucket, and creates a
CloudFront invalidation.

Timeouts are deploy-time parameters. Defaults match the current production
behavior:

```text
LAMBDA_TIMEOUT_SECONDS=30
WORKER_ACQUIRE_TIMEOUT_SECONDS=10
GHCI_STARTUP_TIMEOUT_SECONDS=30
EVAL_CMD_TIMEOUT_SECONDS=10
HISTORY_CMD_TIMEOUT_SECONDS=5
```

To use a shorter Lambda hard timeout:

```sh
LAMBDA_TIMEOUT_SECONDS=20 \
EVAL_CMD_TIMEOUT_SECONDS=8 \
WORKER_ACQUIRE_TIMEOUT_SECONDS=5 \
./serverless/deploy_prod.sh
```

Keep `LAMBDA_TIMEOUT_SECONDS` at or below 30 seconds because requests are served
synchronously through API Gateway.

To deploy only the infrastructure stack:

```sh
sam build -t serverless/template.yaml
sam deploy \
  -t .aws-sam/build/template.yaml \
  --stack-name haskellito-prod \
  --region us-east-1 \
  --profile haskellito-serverless \
  --s3-bucket haskellito-sam-artifacts-<account-id>-us-east-1 \
  --image-repositories PlaygroundFunction=<account-id>.dkr.ecr.us-east-1.amazonaws.com/haskellito/playground \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset \
  --parameter-overrides \
    SiteName=haskellito \
    LambdaTimeoutSeconds=30 \
    WorkerAcquireTimeoutSeconds=10 \
    GhciStartupTimeoutSeconds=30 \
    EvalCommandTimeoutSeconds=10 \
    HistoryCommandTimeoutSeconds=5 \
    DomainName=haskellito.com \
    CertificateArn=arn:aws:acm:us-east-1:123456789012:certificate/example \
    HostedZoneId=Z1234567890ABC
```

## Static Frontend Content

Build the current Vue app from its existing source directory, then generate
public challenge JSON under `serverless/frontend`:

```sh
cd frontend && npm ci && npm run build
cd ..
python3 serverless/frontend/export_challenges.py
```

Publish both static sources to the S3 site bucket:

```sh
SITE_BUCKET=$(aws cloudformation describe-stacks \
  --stack-name haskellito-prod \
  --query "Stacks[0].Outputs[?OutputKey=='SiteBucketName'].OutputValue | [0]" \
  --output text)

aws s3 sync frontend/dist "s3://$SITE_BUCKET" --delete
aws s3 sync serverless/frontend/public/api "s3://$SITE_BUCKET/api" \
  --delete \
  --content-type application/json \
  --cache-control "public,max-age=300"
```

The deployed CloudFront Function is managed by `serverless/template.yaml`. The
standalone JavaScript file under `serverless/frontend/cloudfront-functions` is a
copy kept for review and local reasoning.

## Outputs

The stack exports these useful values:

```text
SiteBucketName
SiteDistributionId
SiteDistributionDomainName
SiteUrl
PlaygroundApiUrl
CloudFrontHostedZoneId
```

## Notes

- The Docker image uses a Debian Python base image plus `awslambdaric` so it can
  install GHC with `apt`, matching the existing Docker approach.
- The existing backend starts GHCi with `-ghci-script ghci.ghci`, so the image
  copies `backend/ghci/config.hs` to `/var/task/ghci.ghci`.
- This is Option A: a compatibility wrapper around the existing FastAPI app.
  With the generated challenge artifacts, CloudFront can route public challenge
  GET requests to S3 while eval/submit remain on Lambda.
