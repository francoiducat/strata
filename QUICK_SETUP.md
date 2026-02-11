# 🔧 Quick Setup Checklist

Use this checklist to deploy your MkDocs site after merging this PR.

## ☑️ Step 1: Cloudflare DNS (Do This First!)

In your Cloudflare dashboard for `ducatillon.net`:

1. Go to **DNS** → **Records**
2. Click **Add record**
3. Fill in:
   ```
   Type:          CNAME
   Name:          strata
   Target:        francoiducat.github.io
   TTL:           Auto
   Proxy status:  DNS only (gray cloud icon)
   ```
4. Click **Save**

⚠️ **IMPORTANT**: Keep the cloud icon GRAY (DNS only), not orange!

## ☑️ Step 2: Merge This PR

Just merge the PR to `main`. The GitHub Action will run automatically.

## ☑️ Step 3: Watch First Deployment

1. Go to: https://github.com/francoiducat/strata/actions
2. Watch the "Deploy MkDocs to GitHub Pages" workflow run
3. Wait for it to complete (usually 1-2 minutes)

## ☑️ Step 4: Configure GitHub Pages

After the workflow completes:

1. Go to: https://github.com/francoiducat/strata/settings/pages
2. Under **Source**:
   - Select: `Deploy from a branch`
   - Branch: `gh-pages`
   - Folder: `/ (root)`
3. Under **Custom domain**:
   - Enter: `strata.ducatillon.net`
   - Click **Save**
4. Wait for DNS check to pass (green checkmark)
5. After certificate is ready: Enable **Enforce HTTPS**

## ☑️ Step 5: Test Your Site!

Wait 5-10 minutes, then visit:

- ✅ https://strata.ducatillon.net/docs/
- ✅ https://strata.ducatillon.net/docs/QuickStart/
- ✅ https://strata.ducatillon.net/docs/Architecture/

## 🎉 Done!

From now on:
- Edit markdown files in `docs/docs/`
- Push to `main`
- Site updates automatically in ~2 minutes!

---

## 🆘 Having Issues?

### DNS not working?
```bash
# Check if DNS is configured correctly
nslookup strata.ducatillon.net
# Should point to: francoiducat.github.io
```

### Still getting 404?
- Wait 30 minutes for full DNS propagation
- Clear your browser cache
- Try incognito/private window

### Need more help?
- Check `MKDOCS_DEPLOYMENT.md` for detailed troubleshooting
- Check `DNS_CONFIGURATION.md` for DNS specifics
