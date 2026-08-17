# The Windy Project SEO deployment

## Files to upload

Place these at the root of the existing website repository:

- `index.html` — replacement homepage
- `robots.txt` — root crawl rules
- `sitemap.xml` — root XML sitemap
- `bleach-and-blood/index.html` — dedicated game page, producing `https://thewindyproject.com/bleach-and-blood/`

The files reference the site's existing assets at:

- `/favicon.png`
- `/images/hero/hero-background.gif`
- `/images/bleach-and-blood/cover-background.jpg`
- `/images/bleach-and-blood/title-logo.png`
- existing `/images/games/...` files

Do not remove those assets.

## After deployment

1. Open `https://thewindyproject.com/bleach-and-blood/` in a private browser window and make sure it returns HTTP 200 and loads both Bleach & Blood images.
2. Open `https://thewindyproject.com/robots.txt` and confirm the sitemap line is visible.
3. Open `https://thewindyproject.com/sitemap.xml` and confirm both URLs are listed.
4. In Google Search Console, add/verify the domain property for `thewindyproject.com` if it is not already verified.
5. Submit `https://thewindyproject.com/sitemap.xml` in Search Console > Sitemaps.
6. Use Search Console > URL Inspection on both:
   - `https://thewindyproject.com/`
   - `https://thewindyproject.com/bleach-and-blood/`
7. Run **Test live URL**, then **Request indexing** for both pages.
8. Test both pages with Google's Rich Results Test. The homepage contains Organization/WebSite JSON-LD; the game page contains VideoGame, Organization and BreadcrumbList JSON-LD. Do not add fake ratings, review counts or prices just to qualify for a richer result.
9. Wherever you control a Bleach & Blood profile (Steam developer description, IndieDB/ModDB, itch.io, YouTube description, X profile/posts), prefer linking directly to `https://thewindyproject.com/bleach-and-blood/` when the link is specifically about the game. Keep `https://thewindyproject.com/` as the studio/home link.

## Important

A sitemap and indexing request improve discovery but do not guarantee immediate indexing or a specific ranking. The dedicated page is designed to give Google a strong first-party page with a unique title, descriptive text, internal links, canonical URL and structured data.
