# SDI Presence Website Preview

## Overview
This project contains the full HTML source of the [SDI Presence](https://www.sdipresence.com) website — an IT Managed Services Provider built with Webflow.

The single file `www_sdipresence_com_source.html` is served via a lightweight Python HTTP server so it can be previewed inside Replit. Styles, images, and scripts load from Webflow's CDN, so an internet connection is required for full rendering.

## How to run
The **Preview** workflow starts the server automatically:
```
python3 server.py
```
The site is served on port 5000.

## Notes
- The HTML file is a static snapshot; links to other pages on sdipresence.com will navigate away from Replit.
- A few cookie-banner and 404 errors appear in the browser console — these are harmless and caused by domain-authorization checks that expect the live domain.
