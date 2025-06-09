# Publishing Your NeuroKit Package to PyPI

Now that you've prepared your package, here are the steps to publish it to PyPI:

## 1. Register for PyPI Accounts

First, register for accounts on:
- **TestPyPI** (for testing): https://test.pypi.org/account/register/
- **PyPI** (for production): https://pypi.org/account/register/

## 2. Create API Tokens

For security, create API tokens instead of using your password:
1. Log in to your TestPyPI/PyPI account
2. Go to Account Settings → API tokens
3. Create a token with the scope "Entire account (all projects)"
4. Save these tokens securely - you'll only see them once!

## 3. Upload to TestPyPI First (Recommended)

```bash
python -m twine upload --repository testpypi dist/*
```

When prompted, use `__token__` as the username and your TestPyPI token (prefixed with `pypi-`) as the password.

## 4. Test Your Package from TestPyPI

Create a new virtual environment and install your package:

```bash
python -m venv test_env
test_env\Scripts\activate  # On Windows
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ neurokit
```

The extra-index-url ensures dependencies can be found on the main PyPI.

## 5. Upload to Production PyPI

Once you've verified everything works from TestPyPI:

```bash
python -m twine upload dist/*
```

Use `__token__` as the username and your PyPI token (prefixed with `pypi-`) as the password.

## 6. Install from PyPI

After publishing, anyone can install your package with:

```bash
pip install neurokit
```

## Updating Your Package

When you want to release a new version:

1. Update the version number in `__init__.py` and `pyproject.toml`
2. Rebuild the package: `python -m build`
3. Upload the new distribution files: `python -m twine upload dist/*`

## Publishing through GitHub (Recommended)

You can automate the PyPI publishing process using GitHub Actions:

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/neurokit.git
   git push -u origin main
   ```

2. **Set up secrets in your GitHub repository:**
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add two secrets:
     - `PYPI_USERNAME`: Set to `__token__`
     - `PYPI_PASSWORD`: Your PyPI API token

3. **Create a GitHub Release:**
   - Go to your repository → Releases → Create a new release
   - Tag version: `v0.1.0` (must match your package version)
   - Release title: `NeuroKit v0.1.0`
   - Description: Release notes about what's new
   - Click "Publish release"

The GitHub Actions workflow we've set up (in `.github/workflows/publish-to-pypi.yml`) will automatically:
1. Build your package
2. Upload it to PyPI
3. Make it available for users to install via `pip install neurokit`

This way, you can manage your releases through GitHub's interface without manually running publishing commands.
