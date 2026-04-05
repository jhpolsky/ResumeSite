# Claude Code Guidelines for ResumeSite

## Project Overview

This is Joseph H. Polsky's implementation of the **AWS Cloud Resume Challenge** (16-step project).

**Reference:** https://cloudresumechallenge.dev/docs/the-challenge/aws/

**Goal:** Build a full-stack, cloud-hosted resume with S3, CloudFront, Route 53, Lambda, DynamoDB, and API Gateway, with CI/CD automation via GitHub Actions.

---

## Repository Structure

```
ResumeSite/
├── index.html              # Resume content (HTML5, valid)
├── style.css               # Styling (dark mode, professional)
├── PROGRESS.md             # Living log of all 16 challenge steps
├── CLAUDE.md               # This file
└── backend/                # (To be created in Step 13 as separate repo)
    ├── lambda_function.py
    ├── template.yaml
    └── tests/
        └── test_lambda.py
```

---

## Key Decisions

### Design & Styling

- **Color Scheme:** Dark mode with teal accents
  - Background: `#1a1a2e` (navy)
  - Surface: `#16213e` (darker navy)
  - Accent: `#0f9b8e` (teal)
  - Text: `#e0e0e0` (light gray)
  - Text Muted: `#9a9ab0` (muted gray)

- **Typography:**
  - Body: Inter (300/400/600 weights)
  - Headings & Code: Fira Mono (400/500 weights)

- **Layout:**
  - Fixed header/footer (48px each) with teal bottom/top borders
  - Slim 6px teal sidebars (responsive: hidden on screens ≤600px)
  - Center-aligned content max-width 820px

### AWS Configuration

- **Region:** `us-east-1` (required for CloudFront ACM certs)
- **Services Used:**
  - S3 (static website hosting)
  - CloudFront (HTTPS + CDN)
  - Route 53 (DNS)
  - Lambda (visitor counter logic)
  - DynamoDB (visitor count persistence, on-demand billing)
  - API Gateway (HTTP API with CORS)

- **Estimated Monthly Cost (after 6-month free tier):** $1–4/month

### Source Control

- **Frontend Repo:** This repo (ResumeSite)
- **Backend Repo:** Separate GitHub repo (to be created in Step 13)

---

## Current Progress

See **PROGRESS.md** for the authoritative status table.

**Completed (Steps 2–3):**
- ✅ Valid HTML5 resume with Joseph's content
- ✅ Professional CSS styling (dark mode)

**Pending (Steps 4–16):**
- S3 static hosting
- CloudFront + HTTPS
- Route 53 DNS
- JavaScript visitor counter
- DynamoDB table
- Lambda + API Gateway
- Python tests
- SAM infrastructure as code
- Backend source control
- CI/CD automation (both frontend & backend)
- Blog post reflection

---

## Code Standards

### HTML

- Valid HTML5 with proper DOCTYPE, meta tags (charset, viewport), and semantic structure
- All resume content in `.stuff` div
- Visitor counter: `<span id="counter">` (populated by JavaScript in Step 7)

### CSS

- Use CSS custom properties (variables) for theming (registered in `:root`)
- Mobile-first responsive design (test at 600px breakpoint)
- No inline styles in HTML (use CSS classes)
- Comment major sections (/* — Section Name — */)

### JavaScript (Step 7 onwards)

- Fetch API to call Lambda endpoint
- Display count in `<span id="counter">`
- Handle network errors gracefully
- Use CORS-enabled API endpoint from API Gateway

### Python (Lambda)

- Use `boto3` for AWS SDK
- Increment counter atomically in DynamoDB
- Return JSON responses
- Write unit tests with `pytest` + `moto`

### Infrastructure as Code (SAM)

- Define Lambda, API Gateway, and DynamoDB in `template.yaml`
- Use SAM CLI: `sam build && sam deploy --guided`
- Enable CORS on API Gateway for the resume domain

---

## AWS CLI Setup

Before proceeding, ensure AWS CLI is configured:

```bash
aws configure
# Enter: Access Key ID, Secret Access Key, region (us-east-1), output (json)

# Verify:
aws sts get-caller-identity
```

---

## Workflow

### When Adding Files/Features

1. **Update PROGRESS.md** — mark the step as in-progress before starting
2. **Make local changes** — edit/create files in ResumeSite/
3. **Test locally** — open index.html in browser, verify styles, functionality
4. **Commit with clear message** — include both frontend and step number (e.g., "Step 4: Add S3 deployment script")
5. **Update PROGRESS.md** — mark step as complete with date and notes
6. **Push to GitHub** — ready for CI/CD automation (Step 15)

### When Deploying to AWS

1. **Create S3 bucket** (Step 4) — `s3://jpolsky-resume` or similar
2. **Push styling/content** — use AWS CLI or S3 console
3. **Verify locally** — test against the public S3 website URL
4. **Enable CloudFront** (Step 5) — distribute via HTTPS
5. **Configure DNS** (Step 6) — point custom domain to CloudFront

---

## Gotchas & Notes

- **ACM Certificates:** CloudFront requires certs in `us-east-1` only
- **S3 + CloudFront:** Disable direct S3 public access; route all traffic through CloudFront for security
- **CORS:** Ensure API Gateway has CORS enabled for the resume domain
- **DynamoDB Billing:** Use on-demand (pay-per-request) to avoid provisioning costs
- **Free Tier:** S3, CloudFront, Route 53, Lambda, DynamoDB all have generous free tier; free tier expires after 6 months for S3/CloudFront
- **Cost Tracking:** Monitor AWS Billing Dashboard during Steps 4–6; costs should remain $0 during free tier

---

## Useful Commands

```bash
# AWS CLI
aws s3 mb s3://jpolsky-resume
aws s3 cp index.html s3://jpolsky-resume/
aws s3 cp style.css s3://jpolsky-resume/
aws s3api get-bucket-website http-status://jpolsky-resume
aws cloudfront list-distributions

# SAM (Steps 12–14)
sam build
sam deploy --guided
sam logs -n VisitorCounterFunction --tail

# DynamoDB (Step 8)
aws dynamodb describe-table --table-name resume-visitor-count

# Local Testing (Step 7+)
npm install  # If using Node test runner
python -m pytest backend/tests/ -v  # If using Python
```

---

## Resume Content (Reference)

**Joseph H. Polsky**
- Location: 20 Halletts Point Apt 611, Astoria NY 11102
- Email: jhpolsky@gmail.com
- Phone: (585) 750-1946

**Summary:** Software Engineer in Test with 7+ years of experience in API testing, automation frameworks, and CI/CD in healthcare and financial systems.

**Key Skills:** Python, C#, Java, JavaScript | Selenium, Cypress, WebdriverIO | PostgreSQL, Oracle, MSSQL, MongoDB | GitHub Actions, Azure Cloud, Terraform | REST, GraphQL, SOAP | Performance/Load/Regression Testing | Team Leadership | Fluent Spanish & Hebrew

**Education:** Cornell University (BS, Minor in Information Science)

**Experience:**
1. **Memorial Sloan Kettering** (June 2022–Present): Senior test automation for clinical imaging pipelines (FHIR/HL7)
2. **Allvue Systems** (March 2018–June 2022): Built test frameworks for API & UI; led offshore QA team
3. **MLB Advanced Media** (Nov 2015–March 2018): QA lead for electronic baseball systems
4. **Perion Inc.** (Sept 2012–Jan 2013): QA intern; database & API testing

---

## Questions or Clarifications?

- Refer to **PROGRESS.md** for step-by-step status
- Refer to **Challenge docs** for exact requirements: https://cloudresumechallenge.dev/docs/the-challenge/aws/
- Check AWS documentation for service-specific setup (S3, CloudFront, Lambda, etc.)
