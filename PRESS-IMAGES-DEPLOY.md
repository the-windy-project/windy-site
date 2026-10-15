# Bleach & Blood press image publishing

Official press page: https://the-windy-project.github.io/windy-site/bleach-and-blood/press/

## Run the import

1. Open https://github.com/the-windy-project/windy-site/actions/workflows/import-press-images.yml
2. Click **Run workflow** and choose `main`.
3. Watch the job named **import-images**. It downloads the 11 explicitly listed public Drive assets, converts them to WebP, writes `images/bleach-and-blood/press/manifest.json`, and updates the press page and image sitemap.
4. Confirm the final workflow step commits generated files. If a download fails, inspect that asset's permissions and rerun. Never publish guessed or fake image URLs.

## Publish and verify

- Check `images/bleach-and-blood/press/manifest.json` exists on `main`.
- Check the press page visibly displays the generated gallery.
- Open a direct image, for example:
  https://the-windy-project.github.io/windy-site/images/bleach-and-blood/press/bleach-and-blood-screenshot-01.webp
  It must load as an image and return HTTP 200.
- Check `https://the-windy-project.github.io/windy-site/sitemap.xml` and confirm each published asset has a `<image:loc>` URL.
- **GitHub Pages note:** automated commits made with the default `GITHUB_TOKEN` may not automatically trigger a branch-based Pages build. If repository files exist but the public website has not changed, trigger an authorized Pages rebuild/deployment from the Pages settings or its configured Pages workflow. Do not assume that an asset exists publicly because it exists in Git.
- Search Console: inspect the press page and request indexing once it loads with real images; submit the existing sitemap. Search Console does not guarantee Google Images inclusion or a Knowledge Panel image strip.

## External distribution

Use the existing press page URL above as the canonical press-kit link on Steam developer/publisher information (where outbound links are permitted), itch.io, IndieDB, ModDB, creator submissions and email signatures. Keep the full original ZIP and folder in Drive. Those original files and their links are already displayed on the press page.

## Notes

The 160 MB trailer and animation GIF originals stay in Drive, not the Pages Git repository. Images for the gallery are derivative display images, not replacements for the original press files. The import script requires the fixed public file IDs to remain downloadable. GitHub Actions needs repository write permission to commit outputs.
