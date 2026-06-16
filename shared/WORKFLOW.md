<!-- managed:linked-repos -->
## Linked Repositories
- heidicrowe22-cyber/velvet-audit
<!-- /managed:linked-repos -->

# Velvet Hour Audit — Code Workflow

## Repository
- **Remote:** `heidicrowe22-cyber/velvet-audit`

## Branch Strategy
- `main` — production-ready code, protected
- Feature branches: `feat/<short-description>`
- Fix branches: `fix/<short-description>`

## Process
1. Members work on feature branches branched from `main`
2. Commit regularly with clear messages
3. Push feature branch and create a PR to `main`
4. Lead reviews the PR using `gh pr review` or the `merge_pr` tool
5. PRs are squash-merged to keep history clean

## First Time Setup
1. Clone the repo into `/home/team/shared/velvethour-audit`
2. Copy the project files into the cloned repo
3. Add `.gitignore` (node_modules, __pycache__, .env, venv, *.db)
4. Create initial commit on `main` branch
5. Push to remote

## Committing
- Use conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`
- Keep commits atomic (one logical change per commit)
- Don't commit secrets, `.env` files, or large binary assets