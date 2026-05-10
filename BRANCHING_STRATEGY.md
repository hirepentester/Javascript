# Branch Strategy & CI/CD Pipeline

## Branch Overview

Your repository now has three main branches with a structured workflow:

### 1. **working** - Development Branch
- Used for active development and feature work
- All new features and bug fixes start here
- CI pipeline runs on every push (Lint → Test → Build)
- Not production-ready

**Typical flow:**
```bash
git checkout working
git pull origin working
git checkout -b feature/your-feature
# Make changes
git commit -am "Add your feature"
git push origin feature/your-feature
# Create PR to working branch
```

### 2. **staging** - Quality Assurance Branch
- Used for testing before production
- Code is merged from working → staging via Pull Request
- Full CI pipeline runs (Lint → Test → Build)
- Should be stable and ready for testing
- Deploy to staging environment for QA

**Typical flow:**
```bash
# After feature is approved in working branch
git checkout staging
git pull origin staging
git merge origin/working
git push origin staging
```

### 3. **deploy** - Production Branch
- Used for production deployments only
- Code is merged from staging → deploy via Pull Request
- Deploy pipeline runs automatically (triggers deployment)
- Only stable, tested code reaches here
- Protected branch (recommended to enable branch protection)

**Typical flow:**
```bash
# After QA approval in staging
git checkout deploy
git pull origin deploy
git merge origin/staging
git push origin deploy
# Deployment automatically triggered
```

---

## CI/CD Pipeline Stages

### **Lint Stage** (Runs on: working, staging branches)
- Checks code quality using flake8 and pylint
- Verifies Python syntax
- Reports code style issues
- Non-blocking (warnings don't stop pipeline)

### **Test Stage** (Runs after: Lint passes)
- Executes all tests using pytest
- Validates functionality
- Non-blocking (allows build even if no tests)

### **Build Stage** (Runs after: Test completes)
- Installs all dependencies
- Verifies application integrity
- Archives build artifacts
- Creates deployment-ready package

### **Deploy Stage** (Runs on: deploy branch only)
- Deploys to production environment
- Currently configured for manual deployment
- Can be integrated with Heroku, Digital Ocean, AWS, etc.

---

## Workflow Diagram

```
feature branch → working (PR & CI) → staging (PR & CI) → deploy (Automatic Deploy)
                      ↓
                   CI Pipeline
              (Lint→Test→Build)
                      ↓
                  Pass/Fail
```

---

## GitHub Actions Workflows

Three workflows are configured:

1. **ci.yml** - Runs Lint → Test → Build on working/staging
2. **deploy.yml** - Handles production deployment from deploy branch
3. **branch-promotion.yml** - Notifies on successful merges between branches

---

## Setup & Configuration

### Branch Protection Rules (Recommended)

Protect the `deploy` and `staging` branches on GitHub:

1. Go to repository Settings → Branches
2. Add branch protection for `deploy`:
   - ✓ Require a pull request before merging
   - ✓ Require status checks to pass before merging
   - ✓ Dismiss stale pull request approvals
   - ✓ Require code reviews before merging

3. Add branch protection for `staging`:
   - ✓ Require a pull request before merging
   - ✓ Require status checks to pass before merging

### Secrets Configuration

Add secrets to your GitHub repository for deployment:

1. Go to Settings → Secrets and variables → Actions
2. Add required secrets:
   - `DEPLOY_KEY` - API key for your deployment platform
   - Any other platform-specific credentials

### For Heroku Deployment

To deploy to Heroku, add to `deploy.yml`:
```yaml
- name: Deploy to Heroku
  env:
    HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
    HEROKU_APP_NAME: your-app-name
  run: |
    npm install -g heroku
    heroku auth:token
    git push heroku deploy:main
```

---

## Common Commands

### Check Branch Status
```bash
git branch -a
git status
```

### Create Feature Branch
```bash
git checkout working
git pull origin working
git checkout -b feature/my-feature
```

### Push Changes
```bash
git add .
git commit -m "Descriptive commit message"
git push origin feature/my-feature
```

### Merge to Next Branch
```bash
# Create a Pull Request on GitHub, or merge locally:
git checkout staging
git pull origin staging
git merge origin/working
git push origin staging
```

---

## Monitoring & Troubleshooting

### View Workflow Status
- Go to GitHub → Actions tab
- See all workflow runs with status (✅ pass, ❌ fail)

### Fix Linting Issues
```bash
pip install flake8 pylint
flake8 . --show-source
pylint main.py
```

### Fix Test Issues
```bash
pip install pytest
pytest . -v
```

### Debug Deployment
- Check Actions tab for deploy workflow logs
- View deployment history in Actions
- Check production environment logs

---

## Best Practices

1. **Keep commits clean** - One feature/fix per commit
2. **Write descriptive PRs** - Explain what, why, and how
3. **Test locally** - Run lint/test before pushing
4. **Code reviews** - Have at least one approval before merging
5. **Never force push** - To staging/deploy branches
6. **Tag releases** - Create GitHub releases for deploy merges
7. **Monitor deployments** - Check production after deploy

---

## Next Steps

1. ✅ Branches created (working, staging, deploy)
2. ✅ CI/CD workflows configured
3. 📋 Configure branch protection rules on GitHub
4. 🔐 Add deployment secrets to GitHub
5. 🧪 Add tests to your project (pytest)
6. 📝 Document deployment procedures
7. 🚀 Deploy and monitor!
