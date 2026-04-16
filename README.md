# ResumeSite — AWS Cloud Resume Challenge

Joseph H. Polsky's implementation of the [AWS Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/aws/).

Live site: **https://jhpolsky.com**

---

## Stack

| Layer | Service |
|-------|---------|
| Hosting | S3 + CloudFront |
| DNS | Route 53 |
| API | API Gateway (HTTP API) |
| Compute | Lambda (Python 3.12) |
| Database | DynamoDB (on-demand) |
| IaC | AWS SAM |
| CI/CD | GitHub Actions (pending) |

---

## Repo Structure

```
ResumeSite/
├── index.html              # Resume (HTML5)
├── style.css               # Dark mode styles
├── counter.js              # Visitor counter (fetches Lambda endpoint)
├── PROGRESS.md             # Step-by-step challenge status
└── backend/
    ├── lambda_function.py  # Lambda handler — increments DynamoDB counter
    ├── template.yaml       # SAM template (Lambda + API GW + DynamoDB)
    ├── samconfig.toml      # SAM deploy defaults
    ├── requirements-dev.txt
    └── tests/
        ├── conftest.py     # Sets env vars before import
        └── test_lambda.py  # pytest suite (moto mocks DynamoDB)
```

---

## Frontend

### Deploy to S3

```bash
aws s3 cp index.html s3://jpolsky-resume/
aws s3 cp style.css s3://jpolsky-resume/
aws s3 cp counter.js s3://jpolsky-resume/
```

### Invalidate CloudFront Cache

Run this after every S3 upload or the CDN will serve stale files.

```bash
aws cloudfront create-invalidation \
  --distribution-id E12TJ8IYB8OQ13 \
  --paths "/*"
```

---

## Backend

### Run Tests (local, no AWS required)

Tests use [moto](https://github.com/getmoto/moto) to mock DynamoDB — they never hit prod.

```bash
cd backend
pip install -r requirements-dev.txt   # first time only
python -m pytest tests/ -v
```

### Build & Deploy Lambda

Requires SAM CLI. Run from the `backend/` directory.

```bash
cd backend
sam.cmd build                  # Git Bash
sam.cmd deploy                 # uses samconfig.toml defaults, prompts for changeset confirm

# PowerShell / CMD
sam build
sam deploy
```

### Tail Lambda Logs

```bash
sam logs -n VisitorCounterFunction --stack-name resume-backend --tail
```

### Check Live Visitor Count

```bash
aws dynamodb get-item \
  --table-name resume-visitor-count \
  --key '{"id": {"S": "visitors"}}' \
  --region us-east-1
```

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `https://ej6k6nb4fe.execute-api.us-east-1.amazonaws.com/count` | Increment and return visitor count |

CORS is locked to `https://jhpolsky.com`.

---

## AWS Resources

| Resource | Name / ID |
|----------|-----------|
| S3 bucket | `jpolsky-resume` |
| CloudFront distribution | `E12TJ8IYB8OQ13` |
| CloudFormation stack | `resume-backend` |
| DynamoDB table | `resume-visitor-count` |
| Region | `us-east-1` |

test