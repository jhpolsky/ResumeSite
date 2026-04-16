# Cloud Resume Challenge — AWS — Progress Log

Reference: https://cloudresumechallenge.dev/docs/the-challenge/aws/

## Current State

- `index.html` — valid HTML5 resume with Joseph's content, visitor counter placeholder `<span id="counter">`
- `style.css` — existing styles (pink header, light blue sidebars, Cormorant Garamond font) linked from `<head>`
- Hosted locally only — not yet deployed to AWS

---

## Steps

| # | Step | Status | Notes |
|---|------|--------|-------|
| 1 | **Certification** | ⬜ Pending | Add AWS Cloud Practitioner cert to resume when obtained |
| 2 | **HTML** | ✅ Done | `index.html` rewritten as valid HTML5 with Joseph's resume content |
| 3 | **CSS** | ✅ Done | Renamed `.css` → `style.css`, linked from `<head>` |
| 4 | **Static Website (S3)** | ✅ Done | S3 bucket `jpolsky-resume` in us-east-1, SSE-S3 enabled, public access blocked, static website hosting enabled |
| 5 | **HTTPS (CloudFront)** | ✅ Done | CloudFront distribution via CloudFormation, OAI enabled, URL: `https://dyxzysub3hhbp.cloudfront.net/` |
| 6 | **DNS (Route 53)** | ✅ Done | Custom domain → CloudFront A/ALIAS record |
| 7 | **JavaScript Counter** | ✅ Done | `counter.js` fetches API Gateway URL, displays count in `<span id="counter">` |
| 8 | **Database (DynamoDB)** | ✅ Done | `resume-visitor-count` table defined in `backend/template.yaml`, PAY_PER_REQUEST billing |
| 9 | **API (API Gateway + Lambda)** | ✅ Done | HttpApi defined in SAM template, CORS locked to `https://jhpolsky.com`, endpoint: `https://ej6k6nb4fe.execute-api.us-east-1.amazonaws.com/count` |
| 10 | **Python (Lambda)** | ✅ Done | `backend/lambda_function.py` — atomic increment via boto3 update_item, Decimal→int cast, CORS header in response |
| 11 | **Tests** | ✅ Done | All 6 tests passing: `test_count_increments`, `test_count_increment_twice`, `test_response_body_contains_count`, `test_body_is_int`, `test_CORS_headers`, `test_table_missing`. Fixed by adding fake AWS credentials to `conftest.py` — moto requires them even though no real AWS calls are made. |
| 12 | **Infrastructure as Code (SAM)** | ✅ Done | `backend/template.yaml` — DynamoDB + Lambda + HttpApi + IAM; deployed via SAM to stack `resume-backend` in us-east-1; tags: `project=resume` via `samconfig.toml` |
| 13 | **Source Control (Backend)** | ✅ Done | Separate GitHub repo `ResumeBackend` created; `lambda_function.py`, `template.yaml`, `samconfig.toml`, `tests/`, `requirements-dev.txt` all moved there |
| 14 | **CI/CD — Backend** | ✅ Done | `.github/workflows/deploy.yml` — runs pytest on every push; deploys via `sam build && sam deploy --no-confirm-changeset` on push to main using `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` GitHub secrets |
| 15 | **CI/CD — Frontend** | ✅ Done | `.github/workflows/deploy.yml` — on push to master: `aws s3 sync` (index.html, style.css, counter.js only) + `cloudfront create-invalidation` using GitHub Secrets |
| 16 | **Blog Post** | ⬜ Pending | Reflection post (dev.to, Medium, or personal blog) |
| 17 | **React Migration** | ⬜ Future | Rebuild frontend as a React app with interactive elements (e.g. animated skill tags, expandable job sections, dark/light toggle). Wire up Google Docs → GitHub Actions webhook so edits in Docs auto-trigger a CI/CD redeploy. |
| 18 | **IAM Hardening** | ⬜ Future | (1) Replace `joseph` access keys with OIDC federation (GitHub Actions native AWS OIDC — no long-lived keys). (2) Create dedicated `github-actions-backend` and `github-actions-frontend` IAM users/roles scoped to only the permissions SAM/S3/CloudFront actually need. |

---

## Notes & Learnings

| Date | Topic | Note |
|------|-------|------|
| 2026-04-04 | Line endings | Added `.gitattributes` with `* text=auto eol=lf` — always use LF even on Windows for web/Linux-deployed projects |
| 2026-04-04 | SAM vs CLI | Started SAM template from day 1 instead of creating DynamoDB manually — avoids throwaway work when you codify in IaC later |
| 2026-04-04 | JS counter | Step 7 (JS) is listed before the backend steps but can't be fully wired up until API Gateway URL exists — write backend first |
| 2026-04-04 | DynamoDB naming | Hyphens allowed in DynamoDB table names but NOT in CloudFormation logical resource names |
| 2026-04-04 | DynamoDB reserved words | `count` is a reserved word — must use `ExpressionAttributeNames` alias (`#count`) in update expressions |
| 2026-04-04 | Lambda return format | Lambda must return `{ statusCode, body }` dict; body must be a JSON string (`json.dumps()`) for API Gateway to pass it through |
| 2026-04-04 | boto3 | Pre-installed in Lambda Python runtime — no `requirements.txt` needed for it |
| 2026-04-04 | Separate repos | Frontend (ResumeSite) and backend stay in one repo until step 13 — CI/CD pipelines are set up after the code is finalized |
| 2026-04-05 | DynamoDB Decimal | DynamoDB returns numbers as Python `Decimal` type — must cast to `int` before `json.dumps()` or it throws `TypeError: Object of type Decimal is not JSON serializable` |
| 2026-04-05 | DynamoDB inspect | To check live DynamoDB data: `aws dynamodb get-item --table-name resume-visitor-count --key '{"id": {"S": "visitors"}}' --region us-east-1`. Returns item with `"N"` (Number) type for count and `"S"` (String) for id. |
| 2026-04-05 | Backend deploy workflow | Lambda change: `git push` → `sam build && sam deploy`. No CloudFront invalidation needed — CloudFront only caches frontend files, not API responses. |
| 2026-04-05 | requirements split | `requirements.txt` is for Lambda production deps (empty — boto3 is pre-installed in Lambda runtime). `requirements-dev.txt` is for test/dev deps (`pytest`, `moto`, `boto3`). Keep them separate so SAM doesn't bundle test deps into the Lambda package. |
| 2026-04-05 | TABLE_NAME env var in tests | `lambda_function.py` reads `TABLE_NAME` at import time — not inside the handler. When running pytest locally this env var doesn't exist, causing `KeyError`. Fix: set `os.environ['TABLE_NAME'] = 'resume-visitor-count'` in the test file before importing `lambda_handler`. |
| 2026-04-05 | moto mock_aws | Use `@mock_aws` decorator from `moto` to intercept all boto3 calls in tests. Must `create_table` inside the test to create a fake DynamoDB table, then `put_item` to seed initial data before calling the handler. moto resets state between tests so each test needs its own table setup. |
| 2026-04-05 | conftest.py | pytest loads `conftest.py` before any test file — use it to set env vars at module level (not in a fixture) so they're available when `lambda_function.py` is imported. Setting in a fixture is too late because the module-level `os.environ['TABLE_NAME']` in lambda_function.py runs at import time. |
| 2026-04-05 | ALLOWED_ORIGIN | Made CORS origin configurable via `os.environ['ALLOWED_ORIGIN']` in Lambda — set in `template.yaml` for AWS, in `conftest.py` for local tests, and will be set in GitHub Actions env for CI/CD. |
| 2026-04-05 | API security | Endpoint is publicly accessible — no auth, no rate limiting. Anyone can inflate the counter. Acceptable for this project. Could add AWS WAF rate limiting later. Worth mentioning in blog post. |
| 2026-04-05 | Remaining tests | TODO: (1) call Lambda twice, assert count == 2 — verifies ADD increments not sets. (2) call Lambda with no table, assert 500 — verifies error handling. (3) assert `json.loads(response['body'])` is `int` — verifies type correctness. |
| 2026-04-05 | Frontend deploy workflow | Frontend change: `git push` → `aws s3 cp <file> s3://jpolsky-resume/` → `aws cloudfront create-invalidation --distribution-id E12TJ8IYB8OQ13 --paths "/*"` |
| 2026-04-16 | moto credentials | moto patches at the HTTP/botocore layer so it intercepts calls even from module-level boto3 objects. But boto3 still needs credentials present to sign requests — without them you get `NoCredentialsError` caught by `except Exception` → silent 500. Fix: add `AWS_ACCESS_KEY_ID=testing`, `AWS_SECRET_ACCESS_KEY=testing`, `AWS_SESSION_TOKEN=testing` to `conftest.py`. moto recognizes these as dummy values and won't hit real AWS. |
| 2026-04-16 | Module-level boto3 in Lambda | `boto3.resource()` and `.Table()` at module level don't make HTTP calls — they just create reference objects. The actual HTTP call happens when a method like `update_item()` is called. So module-level initialization doesn't break moto as long as credentials are set before the call executes. |
| 2026-04-16 | conftest.py load order | conftest.py is loaded before test file imports. Because `lambda_function.py` reads `os.environ['TABLE_NAME']` at module level (line 6), the env var must be set in conftest.py at module level — not inside a pytest fixture — or the import will `KeyError` before any fixture runs. |
| 2026-04-16 | CI/CD backend pipeline | Backend GitHub Actions: `test` job runs pytest on every branch push. `deploy` job gates on `test` passing AND `github.ref == refs/heads/main`. Uses `aws-actions/setup-sam@v2` + `aws-actions/configure-aws-credentials@v4`. SAM deploy uses `--no-confirm-changeset` so it doesn't wait for manual approval. |

---

## Log

| Date | Step(s) | What happened |
|------|---------|---------------|
| 2026-04-04 | 2, 3 | Fixed `index.html` to valid HTML5 with Joseph's resume content; renamed `.css` → `style.css` |
| 2026-04-04 | 4 | Created S3 bucket `jpolsky-resume` in us-east-1 with SSE-S3, blocked public access, uploaded resume files, enabled static website hosting |
| 2026-04-04 | 5 | Starting CloudFront + ACM certificate setup |
| 2026-04-04 | 6 | Custom domain live via Route 53 A/ALIAS record → CloudFront |
| 2026-04-04 | 7 | `counter.js` created — fetch() → API GW → display count; `<script src="counter.js">` in index.html |
| 2026-04-04 | 8, 10, 12 | `backend/template.yaml` started (DynamoDB + Lambda); `backend/lambda_function.py` written — atomic increment, JSON response |
| 2026-04-04 | 9, 12 | SAM deploy initiated via `sam deploy --guided`. Choices: stack name `resume-backend`, region `us-east-1`, confirm changesets `y`, rollback enabled, no auth on Lambda API (intentional — public visitor counter), saved config to `samconfig.toml`. SAM auto-created a managed S3 bucket (`aws-sam-cli-managed-default-samclisourcebucket-9vlmeovjmi66`) to store Lambda artifacts. CloudFormation created 6 resources: DynamoDB table, Lambda function, IAM execution role, HttpApi (ApiGatewayV2 API + default stage), and Lambda invoke permission. Tags (`project=resume`) added to `samconfig.toml` under `[default.deploy.parameters]` — note: stack-level tags cannot go in `template.yaml` (invalid CFN property at top level), must go in `samconfig.toml`. |
| 2026-04-05 | 11 | Started pytest test suite — 3 tests passing. Created `conftest.py` for env var setup, `requirements-dev.txt` for test deps. Refactored CORS origin to env var `ALLOWED_ORIGIN`. Remaining tests noted above. |
| 2026-04-16 | 11, 13, 14 | All 6 tests passing after adding fake AWS credentials to `conftest.py` — moto requires them even though no real AWS is contacted. Steps 13 (separate backend repo) and 14 (CI/CD backend workflow) were already complete but not marked done. Backend CI/CD pipeline: pytest on every push, SAM deploy on merge to main. |
| 2026-04-05 | 7, 9, 10, 12 | Fixed several bugs to get counter working end-to-end: (1) `template.yaml` had `Runtime: python 3.12` with a space — corrected to `python3.12`. (2) Lambda was missing DynamoDB permissions — added `DynamoDBCrudPolicy` SAM policy with `TableName: !Ref VisitorCountTable`. (3) `TABLE_NAME` env var was hardcoded string — changed to `!Ref VisitorCountTable` so policy and env var resolve consistently at deploy time. (4) `lambda_function.py` was hardcoding table name — updated to use `os.environ['TABLE_NAME']`. (5) Lambda response missing CORS header — added `Access-Control-Allow-Origin: https://jhpolsky.com` to return dict. (6) `counter.js` still had placeholder URL `mycounturl` — updated to real API endpoint `https://ej6k6nb4fe.execute-api.us-east-1.amazonaws.com/count`. (7) `index.html` with `<script src="counter.js">` had never been pushed to S3 — counter.js was loading from wrong branch (master vs feature/backend). Pushed correct versions of both files. (8) Hit 500 error on API call — Lambda crashing because DynamoDB returns numbers as Python `Decimal` type which `json.dumps()` can't serialize — fixed by casting to `int`: `int(response['Attributes']['count'])`. (9) CloudFront was serving stale `index.html` and `counter.js` — ran `aws cloudfront create-invalidation --distribution-id E12TJ8IYB8OQ13 --paths "/*"` to flush cache after each S3 push. (10) Git Bash cannot run `sam` directly — SAM CLI installs as a `.cmd` file not natively executable in Bash; use `sam.cmd` in Git Bash or use PowerShell for SAM commands. After all fixes, visitor counter live and incrementing correctly at `https://jhpolsky.com`. Steps 7, 9, 10, 12 complete. |

