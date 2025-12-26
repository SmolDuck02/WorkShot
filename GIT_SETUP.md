# 📦 Git Setup & Upload Instructions

Follow these steps to upload WorkShot to GitHub.

---

## 🚀 Quick Start (First Time)

### 1. Create GitHub Repository

Go to [GitHub](https://github.com/new) and create a new repository:

- **Repository name**: `workshot`
- **Description**: "⚡ Real-time activity tracker for Windows with beautiful futuristic dashboard"
- **Visibility**: Public (for open-source) or Private
- **Don't initialize** with README, .gitignore, or license (we already have them)

---

### 2. Initialize Local Git Repository

Open PowerShell in the `WorkShot` folder and run:

```powershell
# Navigate to WorkShot directory (if not already there)
cd C:\Users\0525\WorkShot\WorkShot

# Initialize git repository
git init

# Configure your identity (if not done globally)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

### 3. Add Files to Git

```powershell
# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status

# Commit with a meaningful message
git commit -m "Initial commit: WorkShot v1.0 - Real-time activity tracker"
```

---

### 4. Connect to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```powershell
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/workshot.git

# Verify remote
git remote -v
```

---

### 5. Push to GitHub

```powershell
# Push to main branch
git branch -M main
git push -u origin main
```

Enter your GitHub credentials when prompted.

---

## 🔐 Authentication Options

### Option 1: Personal Access Token (Recommended)

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "WorkShot Development"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. When pushing, use the token as your password

### Option 2: GitHub CLI (Easiest)

```powershell
# Install GitHub CLI
winget install --id GitHub.cli

# Authenticate
gh auth login

# Push (will use authenticated session)
git push -u origin main
```

### Option 3: SSH Key

```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub | clip

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

Then use SSH URL:
```powershell
git remote set-url origin git@github.com:YOUR_USERNAME/workshot.git
```

---

## 📝 Common Git Commands

### Making Changes

```powershell
# See what changed
git status

# See specific changes
git diff

# Add specific files
git add tracker/monitor.py

# Add all changes
git add .

# Commit changes
git commit -m "Add feature: Export to PDF"

# Push to GitHub
git push
```

---

### Creating Branches

```powershell
# Create and switch to new branch
git checkout -b feature/new-dashboard-theme

# List branches
git branch

# Switch branches
git checkout main

# Push new branch to GitHub
git push -u origin feature/new-dashboard-theme
```

---

### Viewing History

```powershell
# View commit history
git log

# View compact history
git log --oneline

# View specific file history
git log -- tracker/monitor.py
```

---

### Undoing Changes

```powershell
# Discard changes to a file
git checkout -- tracker/monitor.py

# Unstage a file
git reset HEAD tracker/monitor.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - CAREFUL!
git reset --hard HEAD~1
```

---

## 🌿 Branching Strategy

### For Solo Development

```
main (production-ready code)
  ├── feature/export-pdf
  ├── feature/custom-themes
  └── bugfix/idle-detection
```

### Workflow

1. **Create branch** for each feature/bugfix
   ```powershell
   git checkout -b feature/new-feature
   ```

2. **Make changes** and commit regularly
   ```powershell
   git add .
   git commit -m "Progress on new feature"
   ```

3. **Merge to main** when done
   ```powershell
   git checkout main
   git merge feature/new-feature
   ```

4. **Delete branch** after merging
   ```powershell
   git branch -d feature/new-feature
   ```

5. **Push to GitHub**
   ```powershell
   git push
   ```

---

## 🏷️ Versioning (Tags)

### Create Releases

```powershell
# Tag current commit
git tag -a v1.0.0 -m "WorkShot v1.0.0 - Initial Release"

# Push tags to GitHub
git push --tags

# List tags
git tag
```

### Version Naming (Semantic Versioning)

- `v1.0.0` - Major release (breaking changes)
- `v1.1.0` - Minor release (new features)
- `v1.1.1` - Patch release (bug fixes)

---

## 📋 Pre-Commit Checklist

Before pushing to GitHub:

- [ ] **Test the application** - Make sure it runs
- [ ] **Update README** if functionality changed
- [ ] **Check .gitignore** - No sensitive files committed
- [ ] **Write meaningful commit message**
- [ ] **Run linting** (if applicable)
- [ ] **Update version** number in appropriate files

---

## 🐛 Troubleshooting

### "Repository not found" error

```powershell
# Check remote URL
git remote -v

# Update remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/workshot.git
```

---

### "Permission denied" error

- Check your GitHub username/token
- Verify repository access
- Try SSH instead of HTTPS (or vice versa)

---

### "Large files" warning

```powershell
# Remove file from Git history
git rm --cached workshot.db

# Add to .gitignore
echo "workshot.db" >> .gitignore

# Commit and push
git commit -m "Remove database from Git"
git push
```

---

### "Merge conflict" error

```powershell
# See conflicted files
git status

# Edit files to resolve conflicts
# (Look for <<<<<<, =======, >>>>>> markers)

# After fixing:
git add .
git commit -m "Resolve merge conflicts"
```

---

## 🌐 Post-Upload Tasks

After successful upload to GitHub:

### 1. Update Repository Settings

- [ ] Add repository description
- [ ] Add topics/tags: `activity-tracker`, `windows`, `python`, `productivity`
- [ ] Enable Issues and Discussions
- [ ] Set up branch protection (optional)

### 2. Create Release

- [ ] Go to Releases → Create a new release
- [ ] Tag: `v1.0.0`
- [ ] Title: "WorkShot v1.0.0 - Initial Release"
- [ ] Description: Copy from CHANGELOG or README highlights
- [ ] Attach binaries (if applicable)

### 3. Update README Links

Replace placeholder links in README.md:
- `https://github.com/yourusername/workshot` → Your actual URL
- `your.email@example.com` → Your actual email
- Add screenshot URLs

### 4. Promote Your Project

- [ ] Share on Twitter, LinkedIn
- [ ] Post on Reddit (r/Python, r/productivity)
- [ ] Submit to Product Hunt
- [ ] Share on Hacker News (Show HN)
- [ ] Write a blog post

---

## 📚 Additional Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Book](https://git-scm.com/book/en/v2)
- [GitHub CLI](https://cli.github.com/)
- [Semantic Versioning](https://semver.org/)

---

## ✅ Quick Reference

```powershell
# First time setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/workshot.git
git branch -M main
git push -u origin main

# Regular workflow
git add .
git commit -m "Add new feature"
git push

# Create new feature
git checkout -b feature/name
# ... make changes ...
git add .
git commit -m "Implement feature"
git push -u origin feature/name
# Create Pull Request on GitHub
```

---

**Questions?** Check [GitHub Support](https://support.github.com/) or open an issue!

🚀 **Happy coding!** ⚡





