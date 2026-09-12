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

## Contact form

The contact form on the home page sends email via [Web3Forms](https://web3forms.com) —
a free service that relays form submissions to `hello@focuspsychology.com`, with no
server or backend code required. It's already configured and working (tested live).

If the access key ever needs changing (e.g. a new Web3Forms account), it's the
`value` on this line in `index.html`, near the contact form:

```html
<input type="hidden" name="access_key" value="...">
```

Get a new key at <https://web3forms.com>. The form falls back to a "please email us
directly" message if the key is ever missing or invalid, rather than failing silently.

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

- Colour palette is sampled from the 2026 rebrand postcard (`brand/postcard-2026.pdf`).
  The hero image (`assets/img/hero-portrait.png`) is a cropped, optimised export of the
  portrait artwork from that same postcard.
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
  LinkedIn has been removed from contact/footer at the client's request.
- The client testimonial is unchanged in wording, now attributed to "High Hazels
  Academy, Sheffield" only (no individual named), per instruction.
- The "Why Choose Us" section is written around the "Slow Cooker Psychology" concept
  (embedding in schools for gradual, lasting change rather than quick fixes) — the
  phrase used internally/on the 2026 postcard.
- The "no referrals from parents/carers" notice has its own prominent banner section
  (between Services and Contact) rather than being a small note inside a service card.
- The nav switches to the hamburger menu at 900px (not the narrower 720px content
  breakpoint) — the full horizontal nav wraps messily below ~880px, so it hands off to
  the mobile menu earlier than the rest of the layout needs to stack.
