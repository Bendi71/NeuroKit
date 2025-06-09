# GitHub Publishing Guide for NeuroKit

This guide provides step-by-step instructions for publishing your NeuroKit package through GitHub and PyPI.

## Step 1: Push Your Code to GitHub

1. Create a new repository on GitHub:
   - Go to https://github.com/new
   - Name it "neurokit"
   - Set it to public
   - Don't initialize with a README (we already have one)
   - Click "Create repository"

2. Push your local repository to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/neurokit.git
   git push -u origin main
   ```
   Replace `YOUR_USERNAME` with your GitHub username.

## Step 2: Set Up PyPI Secrets in GitHub

1. Create a PyPI account if you don't have one:
   - Go to https://pypi.org/account/register/

2. Generate an API token on PyPI:
   - Log in to PyPI
   - Go to Account Settings → API tokens
   - Create a token with the scope "Entire account (all projects)"
   - Copy the token (you'll only see it once!)

3. Add the token as a secret in your GitHub repository:
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add two secrets:
     - Name: `PYPI_USERNAME` | Value: `__token__`
     - Name: `PYPI_PASSWORD` | Value: Your PyPI API token

## Step 3: Create a GitHub Release

1. Go to your repository on GitHub
2. Click on "Releases" on the right side
3. Click "Create a new release"
4. Set tag version to "v0.1.0" (must match your package version in __init__.py)
5. Title: "NeuroKit v0.1.0"
6. Add a description of your release
7. Click "Publish release"

## Step 4: Watch the Automated Publishing Process

1. After creating the release, GitHub Actions will automatically run:
   - Go to your repository → Actions tab
   - You should see the "Publish to PyPI" workflow running
   - Wait for it to complete successfully

2. Check your package on PyPI:
   - Go to https://pypi.org/project/neurokit/
   - Your package should be listed with the version you just released

## Step 5: Update and Release New Versions

When you're ready to release a new version:

1. Update the version number in both:
   - `__init__.py` (the `__version__` variable)
   - `pyproject.toml` (the `version` field)

2. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Bump version to X.Y.Z"
   git push
   ```

3. Create a new GitHub release with the matching tag (vX.Y.Z)

The GitHub Actions workflow will automatically build and publish the new version to PyPI.
