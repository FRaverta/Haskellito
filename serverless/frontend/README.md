# Serverless Frontend Artifacts

This directory owns frontend-related serverless artifacts without modifying the
existing `frontend/` source tree.

## Public Challenge JSON

Generate static challenge metadata from the existing backend challenge source:

```sh
python3 serverless/frontend/export_challenges.py
```

The generated files are written under:

```text
serverless/frontend/public/
```

S3-compatible files for the current challenge API calls are generated here:

```text
serverless/frontend/public/api/v2/playground/challenges/index.json
serverless/frontend/public/api/v2/playground/challenges/index.en.json
serverless/frontend/public/api/v2/playground/challenges/index.es.json
serverless/frontend/public/api/v2/playground/challenges/<challenge-id>.json
serverless/frontend/public/api/v2/playground/challenges/<challenge-id>.en.json
serverless/frontend/public/api/v2/playground/challenges/<challenge-id>.es.json
```

The deployed CloudFront Function is managed by `serverless/template.yaml`. The
copy at `serverless/frontend/cloudfront-functions/rewrite_challenge_json.js`
documents the rewrite logic for review. It rewrites the current frontend URLs:

```text
/api/v2/playground/challenges
  -> /api/v2/playground/challenges/index.json

/api/v2/playground/challenges?lang=en
  -> /api/v2/playground/challenges/index.en.json

/api/v2/playground/challenges/<id>?lang=es
  -> /api/v2/playground/challenges/<id>.es.json
```

These objects contain only public fields:

- `id`
- `title`
- `description`
- `starter_code`
- `test_count`

Hidden tests and reference solutions are not exported.

## Deploy Shape

Build the existing Vue app normally:

```sh
cd frontend && npm ci && npm run build
```

Then publish both static sources to the same S3 site bucket:

```sh
aws s3 sync frontend/dist "s3://$SITE_BUCKET" --delete
aws s3 sync serverless/frontend/public/api "s3://$SITE_BUCKET/api" \
  --delete \
  --content-type application/json \
  --cache-control "public,max-age=300"
```

The frontend source remains unchanged. CloudFront decides whether a request is
served from S3 or forwarded to Lambda.

Expected CloudFront behavior order:

```text
/api/v2/playground/challenges/*/submit -> Lambda/API origin
/api/v2/playground/challenges*         -> S3 origin + rewrite function
/api/*                                 -> Lambda/API origin
/*                                     -> S3 origin
```

## Local Edge Mode

To mimic the final serverless routing locally, run SAM as the Lambda/API origin
and use `local_edge.py` as the local CloudFront/S3 router.

Terminal 1:

```sh
sam build -t serverless/template.yaml
sam local start-api -t .aws-sam/build/template.yaml --port 3000
```

Terminal 2:

```sh
cd frontend
npm ci
VITE_AUTH_ENABLED=false npm run build
cd ..
python3 serverless/frontend/export_challenges.py
python3 serverless/frontend/local_edge.py \
  --port 8080 \
  --api-origin http://127.0.0.1:3000
```

Open:

```text
http://127.0.0.1:8080
```

Local routing:

```text
GET  /api/v2/playground/challenges*          -> local static JSON
POST /api/v2/playground/challenges/*/submit  -> SAM local Lambda
POST /api/*                                  -> SAM local Lambda
GET  /*                                      -> frontend/dist SPA files
```
