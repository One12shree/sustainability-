# The Sustainabilist

Svelte 5 + SvelteKit static generation using `@sveltejs/adapter-static`.

The homepage uses the supplied saved page, local images and original publication styles. All 618 article links lead to the original content. Search submits to the publication; newsletter signup uses its original Mailchimp endpoint. No WordPress scripts are loaded.

## Run

```sh
npm install
npm run dev
```

## Validate and export

```sh
npm run check
npm run build
npm run preview
```

Deploy the `build/` directory to any static host. No application server is required.

The source snapshot is `src/lib/homepage.json`; Svelte interactions are in `src/routes/+page.svelte`. Assets are in `static/assets/`. Three Instagram thumbnails missing from the supplied folder were omitted. The external live site and newsletter endpoint availability are outside this static project.

Header icons now open local `/ramadan/`, `/contribute/`, and `/our-issues/` pages, recreated from the original public page layouts. Forms on those pages are presentation only and do not submit. Original WordPress scripts and CAPTCHA frames are omitted.
