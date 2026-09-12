# FocusPsychology website

Static site for [focuspsychology.com](https://focuspsychology.com), hosted on Cloudflare Pages.

Plain HTML/CSS/JS — no build step, no framework, no dependencies to install.

## Structure

```
index.html              Home page (all sections)
privacy-policy.html     Privacy policy page
assets/
  css/style.css         All styling
  js/main.js            Mobile nav + contact form submission
  img/                  Logo, favicon
brand/
  postcard-2026.pdf     2026 rebrand postcard — source of the colour palette/style
```

## Editing content

Both pages are plain HTML — open them in any editor and edit the text/markup directly.
Shared styling lives in `assets/css/style.css`; colours are defined as CSS variables at the
top of that file (`:root { --navy: ...; --royal: ...; }` etc.) if you ever want to adjust
the palette.

## Contact form setup (required)

The contact form on the home page sends email via [Web3Forms](https://web3forms.com) —
a free service that relays form submissions to an email address, with no server or
backend code required.

**One-time setup:**

1. Go to <https://web3forms.com> and enter `hello@focuspsychology.com` to generate a
   free access key (no account/password needed — the key is emailed to that address).
2. Open `index.html`, find this line near the contact form:
   ```html
   <input type="hidden" name="access_key" value="REPLACE_WITH_WEB3FORMS_ACCESS_KEY">
   ```
3. Replace `REPLACE_WITH_WEB3FORMS_ACCESS_KEY` with the real key.
4. Commit and push — Cloudflare Pages will redeploy automatically.

Until this is done, the form will show a message asking visitors to email directly
instead of failing silently.

The form also includes a hidden honeypot field (`botcheck`) to deter spam bots —
no action needed, it works automatically.

## Deploying (Cloudflare Pages)

This repo can be connected directly to Cloudflare Pages:

1. Push this repo to GitHub (or GitLab).
2. In the Cloudflare dashboard: **Workers & Pages → Create → Pages → Connect to Git**.
3. Select this repository.
4. Build settings:
   - **Framework preset:** None
   - **Build command:** (leave blank)
   - **Build output directory:** `/`
5. Deploy. Every push to the main branch will redeploy automatically.

No environment variables or secrets are needed for the current setup.

## Local preview

No build tools required — any static file server works, e.g.:

```bash
python3 -m http.server 8420
```

Then open <http://localhost:8420>.

## Notes on this redesign (2026)

- Colour palette and abstract circle/shape motifs are derived from the 2026 rebrand
  postcard (`brand/postcard-2026.pdf`).
- The logo (`assets/img/logo.png`) is unchanged from the previous site, as required.
- The two old stock photos (a "magnifying glass over a digital brain" image and a
  "butterfly behind bars" image) were replaced with custom SVG icons in the new palette —
  the originals felt dated and off-brand against the new visual style. They are not
  included in this repo; ask if you'd like them reinstated.
- The British Psychological Society / HCPC accreditation badges that were on the old
  site were already broken (404) before this rebuild, so they were not carried over.
  Supply current badge files if you'd like them added back.
- The old "mailto:" based enquiry link has been replaced with a working contact form
  (see above). All contact references now point to `hello@focuspsychology.com`.
- The client testimonial is unchanged in wording, now attributed to "High Hazels
  Academy, Sheffield" only (no individual named), per instruction.
