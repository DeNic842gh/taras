# Lab 1 — Git & GitHub workflow

**No commits were made by the template setup.** Run the steps below when you are ready to submit.

## 1. Create an empty GitHub repository

1. Open https://github.com/new
2. Name it (e.g. `fastapi-project-template`)
3. Leave it **empty** (no README, no .gitignore, no license)
4. Copy the repository URL

Optional: install [GitHub CLI](https://cli.github.com/) and run:

```powershell
gh auth login
gh repo create fastapi-project-template --public --source=. --remote=origin
```

## 2. Initialize Git in this folder only

If Git was initialized in a parent directory by mistake, use a repo only here:

```powershell
cd c:\Users\Denis\Desktop\taras
git init
git remote add origin https://github.com/YOUR_USER/fastapi-project-template.git
```

## 3. Production branch (`main`)

```powershell
git checkout -b main
git add .
git commit -m "feat: add FastAPI project template with Poetry"
git push -u origin main
```

## 4. Development branch (`dev`)

```powershell
git checkout -b dev
git log --oneline --graph --decorate --all > git_logs.txt
git add git_logs.txt
git commit -m "docs: add git log snapshot for dev branch"
git push -u origin dev
```

The template already includes `git_logs.txt` as a placeholder; **replace it** with the output of `git log` after your first commit on `dev`, then commit again if your instructor requires a real log file.

## 5. Verify branches

```powershell
git branch -a
git log --oneline --graph --all
```

Expected:

- `main` — production-ready template (no `git_logs.txt` required on prod if you only add it on `dev`)
- `dev` — same template **plus** `git_logs.txt`

To keep `main` without `git_logs.txt`: commit template on `main` first, then branch `dev` and add `git_logs.txt` only there.
