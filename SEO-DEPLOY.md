# Free GitHub Pages migration: Bleach & Blood

## Proposed free site URL

- Studio: https://the-windy-project.github.io/windy-site/
- Game: https://the-windy-project.github.io/windy-site/bleach-and-blood/
- Sitemap: https://the-windy-project.github.io/windy-site/sitemap.xml

These URL paths become usable only after this PR is merged and GitHub Pages is configured. No paid domain is required.

## Publish and detach expired domain

1. Merge the migration pull request into main.
2. In the GitHub repository **Settings → Pages**, confirm publishing from main, /(root) (or preserve an existing working GitHub Pages publishing workflow). If disabled, select 'Deploy from a branch' and main /(root), then Save.
3. In **Settings → Pages**, under **Custom domain**, use **Remove** to detach the old `thewindyproject.com` domain if it is still displayed. This is a required manual setting change; the CNAME deletion in this PR alone should not be assumed to remove the setting.
4. Wait for Pages deployment and confirm both URLs above load in an incognito window, with working images, CSS and links. Do not publish the proposed links externally until these checks pass.
5. Verify that the canonical, Open Graph, JSON-LD, and sitemap URLs all use https://the-windy-project.github.io/windy-site/ and never the expired paid domain.

## Search Console on the free site

1. Open https://search.google.com/search-console/ and add the **URL prefix** property `https://the-windy-project.github.io/windy-site/` (not a DNS-based Domain property; you do not own the shared `github.io` parent domain).
2. Use **HTML file upload** verification. Obtain the exact verification HTML filename and content from Google, commit the file at this repository's root, and verify that it loads at `https://the-windy-project.github.io/windy-site/YOUR-GOOGLE-VERIFICATION-FILE.html` before clicking Verify. Alternatively use Google's HTML meta-tag verification in index.html.
3. Submit `https://the-windy-project.github.io/windy-site/sitemap.xml` under Sitemaps.
4. Use URL Inspection on `https://the-windy-project.github.io/windy-site/` and `https://the-windy-project.github.io/windy-site/bleach-and-blood/` and request indexing **once** after verifying that the URLs are crawlable.
5. Run Google's Rich Results Test and Schema Markup Validator on the deployed game page. No tool guarantees a Google Knowledge Panel.

## Crawl rules note

GitHub Pages project sites live under `/windy-site/`. Crawlers check robots.txt at the **origin root**, not at the project-path robots.txt URL, so the repository's `/windy-site/robots.txt` is not an origin-level robots policy. Submit the sitemap explicitly in Search Console instead.

## Authority/link updates

Once the Pages deployment works, update first-party profiles that you control (Steam, itch.io, YouTube, IndieDB/ModDB, and relevant game-database external website fields) to point to the free game URL. Update broken domain references; do not claim that any unverified listings were changed. The legacy paid-domain URL can remain in historical articles, but it should not be advertised as the live official site.
