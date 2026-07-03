# Vantward Solutions — GitHub Pages Site

A responsive, dependency-free, one-page website for **vantward.com**.

## Before publishing

Open `index.html` and update:

1. `const MEDIUM_URL = "";` near the bottom of the file. Paste the exact Medium profile or article URL.
2. Review the wording, email address, and venture links.
3. Keep the `CNAME` file in the repository root.

## Local preview

From this folder:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Push to GitHub

Create an empty GitHub repository, then run:

```bash
git init
git add .
git commit -m "Launch Vantward website"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/vantward-site.git
git push -u origin main
```

In GitHub:

1. Open **Repository → Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select **main** and **/(root)**, then save.
4. Under **Custom domain**, enter `vantward.com` and save.
5. Once the certificate is ready, enable **Enforce HTTPS**.

## DNS records for vantward.com

At the domain registrar, remove conflicting apex records and add these four `A` records:

| Type | Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

For `www`, add:

| Type | Host | Value |
|---|---|---|
| CNAME | www | `YOUR_GITHUB_USERNAME.github.io` |

Do not include the repository name in the `www` CNAME target.

## Files

- `index.html` — all layout, styling, and JavaScript
- `assets/vantward-logo.png` — optimized transparent logo
- `assets/favicon.png` — browser icon
- `assets/icon-192.png` and `assets/icon-512.png` — sharing/app icons
- `CNAME` — custom-domain declaration
- `.nojekyll` — serves the static files directly
