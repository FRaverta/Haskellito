# Haskellito Serverless

This directory contains the first serverless deployment path for Haskellito.
It uses AWS SAM to package the existing FastAPI backend as a Lambda container
image with Mangum.

## Shape

```text
CloudFront
  /api/* -> API Gateway HTTP API -> Playground Lambda
  /*     -> S3 static frontend
```

The Lambda image imports the existing `backend/main.py` FastAPI app. This keeps
the initial migration small and lets the current routes continue to work while
the frontend/static challenge routing is moved behind CloudFront.

## Files

```text
serverless/
  template.yaml
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

```sh
sam deploy --guided -t serverless/template.yaml
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
aws s3 sync frontend/dist "s3://$SITE_BUCKET" --delete
aws s3 cp serverless/frontend/public/api "s3://$SITE_BUCKET/api" \
  --recursive \
  --content-type application/json \
  --cache-control "public,max-age=300"
```

Attach `serverless/frontend/cloudfront-functions/rewrite_challenge_json.js` to
the CloudFront behavior that serves public challenge GET requests from S3.

## Notes

- The Docker image uses a Debian Python base image plus `awslambdaric` so it can
  install GHC with `apt`, matching the existing Docker approach.
- The existing backend starts GHCi with `-ghci-script ghci.ghci`, so the image
  copies `backend/ghci/config.hs` to `/var/task/ghci.ghci`.
- This is Option A: a compatibility wrapper around the existing FastAPI app.
  With the generated challenge artifacts, CloudFront can route public challenge
  GET requests to S3 while eval/submit remain on Lambda.
