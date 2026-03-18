# SESSION 3 — Project Collaboration with GitLab

**Duration:** 1h 30min  
**Goal:** Use GitLab effectively for version control, code review, issue tracking, and CI/CD.

---

## 3.1 Git Foundations (Rapid Review)

### Core Concepts

| Concept         | What it means                           |
| --------------- | --------------------------------------- |
| **Repository**  | The full history of your project        |
| **Commit**      | A snapshot of changes with a message    |
| **Branch**      | An independent line of development      |
| **Merge**       | Integrate one branch into another       |
| **Remote**      | A copy of the repo on a server (GitLab) |
| **Clone**       | Download a remote repo locally          |
| **Push / Pull** | Send / receive commits from the remote  |

### Essential Commands

```bash
# Start working on a repository
git clone git@gitlab.com:org/project.git
cd project

# Daily workflow
git status                         # what has changed?
git diff                           # see exact changes
git add src/utils.py               # stage a specific file
git add .                          # stage everything
git commit -m "feat: add date parser utility"
git push origin main

# Branching
git checkout -b feature/user-auth  # create and switch to new branch
git checkout main                  # go back to main
git merge feature/user-auth        # merge feature into main

# Inspecting history
git log --oneline --graph          # visual branch history
git show abc1234                   # show a specific commit
```

### Commit Message Convention

Use **Conventional Commits** — it makes history readable and enables automated changelogs:

```
<type>: <short summary>

[optional body]
[optional footer]
```

| Type       | When to use                     |
| ---------- | ------------------------------- |
| `feat`     | New feature                     |
| `fix`      | Bug fix                         |
| `refactor` | Code change without feature/fix |
| `test`     | Adding or fixing tests          |
| `docs`     | Documentation only              |
| `chore`    | Tooling, dependencies, config   |
| `ci`       | CI/CD pipeline changes          |

```bash
# Good commit messages
git commit -m "feat: add JWT authentication to login endpoint"
git commit -m "fix: handle empty response from weather API"
git commit -m "chore: upgrade fastapi to 0.111"

# Bad commit messages
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "aaa"
```

---

## 3.2 GitLab — Key Features

### GitLab vs GitHub

Both are Git hosting platforms. GitLab's distinguishing features:

- Full built-in CI/CD (no separate GitHub Actions billing model)
- Self-hosted option (popular in enterprises with strict data requirements)
- Built-in container registry
- Built-in security scanning (SAST, dependency scanning)
- Merge Request approvals with granular rules

### GitLab Anatomy

```
GitLab Instance
└── Group (org or team)
    └── Project (repository)
        ├── Repository        ← the code
        ├── Issues            ← task and bug tracking
        ├── Merge Requests    ← code review
        ├── CI/CD Pipelines   ← automated testing and deployment
        ├── Packages          ← container and package registry
        └── Wiki              ← documentation
```

---

## 3.3 The Feature Branch Workflow

This is the standard workflow for teams using GitLab.

```
main ──────●──────────────────────────●──── (protected)
            \                        /
             ●──●──●  feature/login  ↑
                                     MR + review + CI
```

### Step-by-Step

```bash
# 1. Always start from an up-to-date main
git checkout main
git pull origin main

# 2. Create a branch named after the issue or feature
git checkout -b feature/42-user-authentication

# 3. Make changes, commit regularly
git add .
git commit -m "feat: add password hashing with bcrypt"

# 4. Push your branch
git push origin feature/42-user-authentication

# 5. Open a Merge Request on GitLab (via UI or CLI)
# 6. Address review comments, push more commits
# 7. CI passes → reviewer approves → merge
```

### Branch Naming Convention

```
feature/<issue-id>-<short-description>   # new work
fix/<issue-id>-<short-description>       # bug fixes
chore/<description>                      # maintenance
release/<version>                        # release prep
```

---

## 3.4 Merge Requests (MR)

### What Makes a Good MR

A Merge Request should be:

- **Small** — ideally under 400 lines of change; easier to review and revert
- **Focused** — one logical change per MR; do not mix a feature with refactoring
- **Tested** — CI must pass before merge
- **Described** — title and description explain _why_, not just _what_

### MR Description Template

```markdown
## Summary

Brief description of what this MR does and why.

## Changes

- Added `UserAuthService` with bcrypt password hashing
- Integrated auth middleware into FastAPI router
- Added 12 unit tests covering happy and error paths

## Testing

- All existing tests pass
- New tests: `pytest tests/test_auth.py`

## Related Issues

Closes #42
```

### Reviewing a Merge Request

As a reviewer, your checklist:

- Does the code do what the description says?
- Are there tests? Do the tests actually verify the right behaviour?
- Are there security issues? (injection, secrets in code, improper auth)
- Is error handling present and appropriate?
- Is the code readable in 6 months without the author present?
- Does it follow the project's style and conventions?

### Giving Constructive Review Comments

````
# Too vague
"This is wrong."

# Better — specific, actionable, explains why
"This will panic if `response.json()` returns None (e.g. on a 204 response).
Consider adding a None check or using `.get()` with a default."

# Suggestion syntax in GitLab
```suggestion
if data := response.json():
    return parse_result(data)
return None
````

````

---

## 3.5 GitLab CI/CD

### What is CI/CD?

| Term | Meaning |
|------|---------|
| **CI** (Continuous Integration) | Automatically run tests on every push |
| **CD** (Continuous Delivery) | Automatically build and prepare for deployment |
| **CD** (Continuous Deployment) | Automatically deploy to production on merge |

CI catches bugs before humans review the code. It is the first line of defence.

### `.gitlab-ci.yml` — Pipeline Configuration

```yaml
# .gitlab-ci.yml — placed at repository root

stages:
  - lint
  - test
  - build

variables:
  UV_VERSION: "0.4.0"
  PYTHON_VERSION: "3.12"

# ── Lint stage ──────────────────────────────────────────────────────────
ruff:
  stage: lint
  image: python:3.12-slim
  before_script:
    - pip install uv==$UV_VERSION
    - uv sync --dev
  script:
    - uv run ruff check .
    - uv run ruff format --check .

# ── Test stage ───────────────────────────────────────────────────────────
pytest:
  stage: test
  image: python:3.12-slim
  before_script:
    - pip install uv==$UV_VERSION
    - uv sync --dev
  script:
    - uv run pytest --cov=src --cov-report=xml -v
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

# ── Build stage ──────────────────────────────────────────────────────────
build-image:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  only:
    - main
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
````

### Pipeline Stages Explained

```
Push to branch
      ↓
  [lint]  ruff check + format check
      ↓ (only if lint passes)
  [test]  pytest + coverage report
      ↓ (only if tests pass, only on main)
  [build] docker image build and push
```

### Protected Branches and Merge Rules

In GitLab Settings → Repository → Protected Branches:

| Setting                 | Recommended value      |
| ----------------------- | ---------------------- |
| Who can push to `main`  | No one (force MR only) |
| Who can merge to `main` | Maintainers            |
| Require passing CI      | Yes                    |
| Require MR approvals    | 1 or 2 reviewers       |

This ensures no code reaches `main` without passing tests and human review.

---

## 3.6 Issues and Project Management

### Creating Good Issues

An issue should contain:

- **Title** — clear summary of the problem or task
- **Description** — context, expected behaviour, actual behaviour (for bugs)
- **Steps to reproduce** (for bugs)
- **Acceptance criteria** — how do you know it is done?
- **Labels** — `bug`, `feature`, `chore`, `blocked`, etc.
- **Milestone** — sprint or release it belongs to
- **Assignee** — who is responsible

### Issue Templates

Store in `.gitlab/issue_templates/`:

```markdown
<!-- .gitlab/issue_templates/Bug.md -->

## Description

Clear description of the bug.

## Steps to Reproduce

1.
2.
3.

## Expected Behaviour

## Actual Behaviour

## Environment

- Python version:
- OS:
- Relevant package versions:

## Acceptance Criteria

- [ ] Bug no longer reproducible following the steps above
- [ ] Regression test added
```

### Linking Issues to Commits and MRs

```bash
# Closes the issue when the MR merges
git commit -m "fix: correct timezone handling in date parser

Closes #38"

# References without closing
git commit -m "test: add coverage for edge cases (see #38)"
```

---

## 3.7 GitLab Flow — Putting It All Together

```
┌──────────────────────────────────────────────────────┐
│  DAILY WORKFLOW                                      │
│                                                      │
│  1. Pick issue from board                            │
│  2. git checkout -b feature/<id>-<name>              │
│  3. Develop, commit often, push                      │
│  4. Open MR → CI runs automatically                  │
│  5. Fix CI failures, push again                      │
│  6. Reviewer leaves comments                         │
│  7. Address comments, push fixup commits             │
│  8. Reviewer approves + CI green → merge             │
│  9. Branch auto-deleted                              │
│ 10. Issue auto-closed (via "Closes #X")              │
└──────────────────────────────────────────────────────┘
```

### `.gitignore` for Python Projects

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python

# Environments
.venv/
venv/
env/

# UV
# Note: uv.lock should NOT be in .gitignore — commit it!

# Distribution
dist/
build/
*.egg-info/

# Testing
.pytest_cache/
.coverage
coverage.xml
htmlcov/

# IDE
.vscode/settings.json
.idea/

# Secrets
.env
*.pem
*.key
```

---

## Session 3 — Hands-On Exercise (25 min)

### Exercise 3A: Repository Setup (10 min)

1. Create a new project on GitLab (or use the provided one)
2. Clone it locally
3. Add the `weather-cli` project from Session 2 to the repository
4. Add a proper `.gitignore`
5. Commit and push with message: `chore: initial project setup`

### Exercise 3B: Feature Branch and MR (15 min)

1. Create an issue: "Add support for 5-day forecast"
2. Create a branch: `git checkout -b feature/1-five-day-forecast`
3. Make a small change (add a stub function with a docstring)
4. Commit: `git commit -m "feat: add get_forecast stub (see #1)"`
5. Push and open a Merge Request on GitLab
6. Fill in the MR description using the template from section 3.4
7. Add `.gitlab-ci.yml` with the lint and test stages
8. Observe the pipeline run (it may fail — that is expected and instructive)

---
