# GitHub Pages DNS Configuration for strata.ducatillon.net

## Overview
This document explains the DNS configuration needed to make your MkDocs site available at `strata.ducatillon.net/docs`.

## Cloudflare DNS Settings

You need to configure your DNS records in Cloudflare to point `strata.ducatillon.net` to GitHub Pages.

### Option 1: CNAME Record (Recommended if strata is a subdomain)

If `strata.ducatillon.net` is a subdomain:

1. Log in to your Cloudflare dashboard
2. Select your domain `ducatillon.net`
3. Go to **DNS** > **Records**
4. Add the following CNAME record:

| Type  | Name   | Target                    | TTL  | Proxy Status    |
|-------|--------|---------------------------|------|-----------------|
| CNAME | strata | francoiducat.github.io    | Auto | DNS only (gray) |

**Important:** 
- Set Proxy Status to **DNS only** (gray cloud icon) initially to avoid issues with GitHub Pages SSL certificate
- You can enable Cloudflare proxy (orange cloud) after GitHub Pages successfully provisions the SSL certificate

### Option 2: A Records (If strata is an apex domain)

If you're using an apex domain instead, add these A records:

| Type | Name   | Target          | TTL  |
|------|--------|-----------------|------|
| A    | strata | 185.199.108.153 | Auto |
| A    | strata | 185.199.109.153 | Auto |
| A    | strata | 185.199.110.153 | Auto |
| A    | strata | 185.199.111.153 | Auto |

## GitHub Pages Configuration

After setting up DNS:

1. Go to your repository settings: https://github.com/francoiducat/strata/settings/pages
2. Under **Source**, select:
   - Source: `Deploy from a branch`
   - Branch: `gh-pages` 
   - Folder: `/ (root)`
3. Under **Custom domain**, enter: `strata.ducatillon.net`
4. Check **Enforce HTTPS** (after DNS propagates and SSL certificate is issued)

## Verification

1. Wait for DNS propagation (can take up to 24-48 hours, but usually much faster)
2. Check DNS propagation: `nslookup strata.ducatillon.net`
3. Visit: `https://strata.ducatillon.net/docs/`

## How the CNAME File Works

The GitHub Action automatically creates a `CNAME` file in the `gh-pages` branch with the content `strata.ducatillon.net`. This tells GitHub Pages to serve your site at this custom domain.

## Troubleshooting

### DNS Issues
- Use `dig strata.ducatillon.net` or online tools like https://dnschecker.org to verify DNS records
- Ensure Cloudflare proxy is disabled initially (gray cloud)

### SSL Certificate Issues
- GitHub Pages needs to provision an SSL certificate for your custom domain
- This can take a few minutes to several hours
- Don't enable "Enforce HTTPS" until the certificate is ready

### 404 Errors
- Ensure the `gh-pages` branch exists and contains the built site
- Verify the CNAME file is present in the `gh-pages` branch root
- Check that the workflow ran successfully

## Expected URLs

- **Documentation Home:** https://strata.ducatillon.net/docs/
- **Example Page:** https://strata.ducatillon.net/docs/QuickStart/
- **Another Example:** https://strata.ducatillon.net/docs/Architecture/

Note: With `use_directory_urls: true`, MkDocs creates clean URLs without `.html` extensions.
