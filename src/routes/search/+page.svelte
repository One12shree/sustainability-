<script lang="ts">
  import { page } from "$app/state";
  import homepage from "$lib/homepage.json";

  type Result = {
    title: string;
    summary: string;
    image?: string;
    source: string;
  };

  const localPages: Result[] = [
    { title: "About Us", summary: "Learn about The Sustainabilist.", source: "/about-us/" },
    { title: "Our Editor in Chief", summary: "Meet our editor in chief.", source: "/our-editor-in-chief/" },
    { title: "Green Economist's Note", summary: "Insights from our green economist.", source: "/green-economists-note/" },
    { title: "Media Kit", summary: "Media and advertising information.", source: "/media-kit/" },
    { title: "Editorial Calendar", summary: "Our editorial calendar.", source: "/editorial-calendar/" },
    { title: "Trending Articles", summary: "Browse trending sustainability stories.", source: "/trending-articles/" },
    { title: "Themes", summary: "Explore sustainability themes.", source: "/themes/" },
    { title: "Our Partners", summary: "Meet our partners.", source: "/partners/" },
    { title: "Green Jobs", summary: "Explore green job opportunities.", source: "/green-jobs/" },
    { title: "Advertise with us", summary: "Advertising opportunities with The Sustainabilist.", source: "/advertise-with-us/" },
    { title: "Contact Us", summary: "Get in touch with The Sustainabilist.", source: "/contact-us/" },
    { title: "Ramadan", summary: "Low-carbon cooking and Ramadan resources.", source: "/ramadan/" },
    { title: "Recipes", summary: "Low-carbon Ramadan recipes.", source: "/ramadan/recipes/" },
    { title: "Calculate your carbon foodprint", summary: "Calculate the carbon footprint of your diet.", source: "/ramadan/calculate-your-carbon-foodprint/" },
  ];

  function decode(value: string) {
    const textarea = typeof document === "undefined" ? null : document.createElement("textarea");
    if (!textarea) return value.replace(/&amp;/g, "&");
    textarea.innerHTML = value;
    return textarea.value;
  }

  function text(value: string) {
    return decode(value.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim());
  }

  const articlePattern = /<a href="(https:\/\/thesustainabilist\.ae\/[^\"]+)"[^>]*>\s*<div[^>]*>\s*(?:<img[^>]*src="([^\"]+)"[^>]*>)?\s*<div[^>]*>\s*<h2[^>]*>([\s\S]*?)<\/h2>(?:\s*<p[^>]*>([\s\S]*?)<\/p>)?/g;
  const articles: Result[] = Array.from(homepage.body.matchAll(articlePattern)).map(
    ([, source, image, title, summary]) => ({
      title: text(title),
      summary: text(summary || "Read this sustainability story."),
      image,
      source: decode(source),
    }),
  );

  $: query = page.url.searchParams.get("q")?.trim() ?? "";
  $: selectedSource = page.url.searchParams.get("article");
  $: selected = articles.find((article) => article.source === selectedSource);
  $: terms = query.toLocaleLowerCase().split(/\s+/).filter(Boolean);
  $: results = [...localPages, ...articles]
    .filter((result) => terms.every((term) => `${result.title} ${result.summary}`.toLocaleLowerCase().includes(term)))
    .slice(0, 30);
  $: searchUrl = (source: string) =>
    source.startsWith("/")
      ? source
      : `/search/?q=${encodeURIComponent(query)}&article=${encodeURIComponent(source)}`;
</script>

<svelte:head><title>Search | The Sustainabilist</title></svelte:head>

<main class="search-page">
  <a class="back" href="/">← Back to home</a>
  <form action="/search/" method="get" role="search">
    <label for="site-search">Search The Sustainabilist</label>
    <div class="search-input"><input id="site-search" name="q" value={query} placeholder="Search here..." /><button type="submit">Search</button></div>
  </form>

  {#if selected}
    <article class="article-preview">
      <a class="back" href={`/search/?q=${encodeURIComponent(query)}`}>← Back to results</a>
      {#if selected.image}<img src={selected.image} alt="" />{/if}
      <h1>{selected.title}</h1>
      <p>{selected.summary}</p>
      <p class="notice">This article is available in the local search archive.</p>
    </article>
  {:else if query}
    <h1>Search results for “{query}”</h1>
    <p>{results.length} result{results.length === 1 ? "" : "s"} found.</p>
    <section class="results">
      {#each results as result}
        <a class="result" href={searchUrl(result.source)}>
          {#if result.image}<img src={result.image} alt="" />{/if}
          <div><h2>{result.title}</h2><p>{result.summary}</p></div>
        </a>
      {:else}
        <p>No local results matched your search.</p>
      {/each}
    </section>
  {:else}
    <h1>Search the local archive</h1>
    <p>Enter a word or phrase to find pages and articles saved in this site.</p>
  {/if}
</main>

<style>
  .search-page { max-width: 900px; margin: 0 auto; padding: 48px 24px 80px; color: #232629; font-family: Arial, sans-serif; }
  .back { color: #4c9a2a; text-decoration: none; display: inline-block; margin-bottom: 30px; }
  form { margin-bottom: 40px; } label { display: block; font-size: 1.1rem; font-weight: 700; margin-bottom: 10px; }
  .search-input { display: flex; } input { min-width: 0; flex: 1; padding: 13px; border: 1px solid #bfc5bf; font: inherit; } button { padding: 13px 22px; border: 0; background: #51c103; color: white; font: inherit; cursor: pointer; }
  .results { display: grid; gap: 14px; margin-top: 24px; }.result { display: flex; gap: 18px; padding: 16px; color: inherit; text-decoration: none; border: 1px solid #e1e5df; }.result:hover { border-color: #51c103; }.result img { width: 130px; height: 90px; object-fit: cover; }.result h2 { margin: 0 0 7px; font-size: 1.15rem; }.result p { margin: 0; line-height: 1.5; }.article-preview { max-width: 720px; }.article-preview img { width: 100%; max-height: 440px; object-fit: cover; }.notice { color: #5a6559; font-style: italic; } @media (max-width: 560px) { .search-page { padding: 30px 16px; }.result img { width: 90px; height: 70px; } }
</style>
