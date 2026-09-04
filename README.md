# crystalorlando.com

Static site for Crystal Orlando, charcoal and graphite fine artist. No framework, no build dependencies beyond Python 3.

## Layout

```
index.html               home
works/  about/  commissions/  galleries/  faq/  contact/   one index.html each
404.html                 not-found page
fullsite.html            redirect stub for the old URL
assets/css/site.css      all styles
assets/js/site.js        progressive enhancement only (reveals, sticky header)
assets/img/              artwork in WebP + JPEG at several widths
robots.txt  sitemap.xml  llms.txt  site.webmanifest  vercel.json
tools/build.py           generates every HTML page and sitemap.xml
tools/images.py          regenerates assets/img/ from source-images/
```

## Editing copy

All page text, titles, meta descriptions, FAQ answers and structured data live in `tools/build.py`. Edit there, then regenerate:

```
python3 tools/build.py
```

Do not hand-edit the generated HTML files; the next build overwrites them.

## Replacing artwork images

1. Put high-resolution originals in `source-images/` with the filenames listed at the top of `tools/images.py`.
2. `pip install pillow && python3 tools/images.py`
3. Copy the printed `w`, `h` and `sizes` values into the matching `WORKS` entry in `tools/build.py`.
4. `python3 tools/build.py`

`tools/images.py` only rebuilds the six gallery-scale files. The close-up crops
(`guardian-detail`, `horse-detail`, `horse-detail-2`, `bear-detail`) are cut by hand
from the same originals, trimmed to the edge of the artwork with no gallery wall
around them. Recrop those separately and update the `width`/`height` attributes
where they appear in `tools/build.py`. The `w` value of every work also caps how
wide it may render, so a figure is never scaled past its own pixels.

## Local preview

```
npx http-server -p 8123 --ext html .
```

## Deploy

Hosted on Vercel. `vercel.json` enables clean URLs with trailing slashes, redirects the old `/fullsite.html` and `/index.html` URLs to `/`, and sets long cache headers on `/assets/`. Push to the production branch and Vercel deploys the static files as-is.

After a deploy, submit `https://crystalorlando.com/sitemap.xml` in Google Search Console and check `/`, `/works/` and `/faq/` in the Rich Results Test.
