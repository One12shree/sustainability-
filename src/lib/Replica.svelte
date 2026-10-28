<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import initialHomepage from "$lib/homepage.json";
  export let homepage = initialHomepage;
  export let title = "The Sustainabilist";
  export let frontendOnly = false;
  const ramadanLinks: Record<string, string> = {
    "https://thesustainabilist.ae/how-to-eat-low-carbon/":
      "/ramadan/how-to-eat-low-carbon/",
    "https://thesustainabilist.ae/calculate-your-carbon-foodprint/":
      "/ramadan/calculate-your-carbon-foodprint/",
    "https://thesustainabilist.ae/recipe/": "/ramadan/recipes/",
    "https://thesustainabilist.ae/low-carbon-cooking-partners/":
      "/ramadan/low-carbon-cooking-partners/",
  };
  const menuLinks: Record<string, string> = {
    "About Us": "/about-us/",
    "Our Editor in Chief": "/our-editor-in-chief/",
    "Green Economist’s Note": "/green-economists-note/",
    "Media Kit": "/media-kit/",
    "Editorial Calendar": "/editorial-calendar/",
    "Trending Articles": "/trending-articles/",
    Themes: "/themes/",
    "Our Partners": "/partners/",
    "Green Jobs": "/green-jobs/",
    "Advertise with us": "/advertise-with-us/",
    "Contact Us": "/contact-us/",
  };
  $: ramadanBody = Object.entries(ramadanLinks).reduce(
    (html, [from, to]) => html.replaceAll(from, to),
    homepage.body,
  );
  $: menuBody = Object.entries(menuLinks).reduce(
    (html, [label, href]) =>
      html.replaceAll(
        `<span class="menu-label">${label}</span>`,
        `<a class="menu-label" href="${href}">${label}</a>`,
      ),
    ramadanBody,
  );
  $: body = menuBody
    .replaceAll('action="https://thesustainabilist.ae/"', 'action="/search/"')
    .replaceAll('name="s"', 'name="q"')
    .replaceAll('name="phrase"', 'name="q"')
    .replaceAll("name='phrase'", "name='q'")
    .replace(/action=(['"])#\1/g, 'action="/search/"');

  onMount(() => {
    const grid = document.querySelector<HTMLElement>("#grid");
    let frame = 0;
    function layout() {
      if (!grid) return;
      const columns =
        window.innerWidth <= 600 ? 1 : window.innerWidth <= 900 ? 2 : 3;
      grid.classList.add("masonry");
      const width = grid.clientWidth / columns;
      const heights = Array(columns).fill(0);
      for (const element of grid.children) {
        const card = element as HTMLElement;
        card.style.width = `${width}px`;
        const column = heights.indexOf(Math.min(...heights));
        card.style.left = `${column * width}px`;
        card.style.top = `${heights[column]}px`;
        heights[column] += card.getBoundingClientRect().height;
      }
      grid.style.height = `${Math.max(...heights)}px`;
    }
    function schedule() {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(layout);
    }
    const observer = new ResizeObserver(schedule);
    if (grid) for (const card of grid.children) observer.observe(card);
    window.addEventListener("resize", schedule);
    function click(event: MouseEvent) {
      const target = event.target instanceof Element ? event.target : null;
      if (target?.closest(".home-subs")) {
        event.preventDefault();
        const popup = document.querySelector<HTMLElement>(".popup");
        if (popup) {
          popup.style.display = "block";
          popup.setAttribute("role", "dialog");
          popup.setAttribute("aria-label", "Subscribe to The Sustainabilist");
          popup.querySelector<HTMLInputElement>("input[type=email]")?.focus();
        }
      }
      if (target?.closest(".close")) {
        event.preventDefault();
        document
          .querySelectorAll<HTMLElement>(".popup")
          .forEach((p) => (p.style.display = "none"));
      }
      if (target?.closest(".ram")) {
        const panel = document.querySelector<HTMLElement>(".cntram");
        if (panel)
          panel.style.display =
            panel.style.display === "block" ? "none" : "block";
      }
      if (target?.closest(".collapsible")) {
        const button = target.closest(".collapsible");
        const panel = button?.nextElementSibling as HTMLElement | null;
        if (panel) {
          const open = button?.getAttribute("aria-expanded") === "true";
          button?.setAttribute("aria-expanded", String(!open));
          panel.style.maxHeight = open ? "0px" : `${panel.scrollHeight}px`;
          panel.style.overflow = "hidden";
        }
      }
      if (target?.closest(".promagnifier"))
        document
          .querySelector<HTMLFormElement>(".proinput form")
          ?.requestSubmit();
    }
    function key(event: KeyboardEvent) {
      if (event.key === "Escape") {
        document
          .querySelectorAll<HTMLElement>(".popup")
          .forEach((p) => (p.style.display = "none"));
        const menu = document.querySelector<HTMLInputElement>("#menu-switch");
        if (menu) menu.checked = false;
      }
    }
    function input(event: Event) {
      const field = event.target;
      if (!(field instanceof HTMLInputElement) || !field.matches('[role="search"] input[type="search"]')) return;
      const phrase = field.value.trim().toLocaleLowerCase();
      document.querySelector(".local-search-suggestions")?.remove();
      if (!phrase) return;

      const choices = Array.from(document.querySelectorAll<HTMLAnchorElement>("a[href]"))
        .map((link) => ({ title: link.textContent?.replace(/\s+/g, " ").trim() ?? "", href: link.getAttribute("href") ?? "" }))
        .filter((link) => link.title && link.href.startsWith("/") && link.title.toLocaleLowerCase().includes(phrase))
        .filter((link, index, links) => links.findIndex((item) => item.href === link.href) === index)
        .slice(0, 4);
      const suggestions = document.createElement("div");
      suggestions.className = "local-search-suggestions";
      if (choices.length) {
        suggestions.innerHTML = choices
          .map((choice) => `<a href="${choice.href}">${choice.title}</a>`)
          .join("");
      } else {
        suggestions.innerHTML = `<a href="/search/?q=${encodeURIComponent(field.value)}">Search for “${field.value}”</a>`;
      }
      field.closest(".asl_w_container")?.append(suggestions);
    }
    function submit(event: SubmitEvent) {
      const form = event.target;
      if (form instanceof HTMLFormElement && form.matches('[role="search"]')) {
        event.preventDefault();
        const data = new FormData(form);
        const query = (data.get("q") ?? data.get("s") ?? data.get("phrase"))
          ?.toString()
          .trim();
        goto(query ? `/search/?q=${encodeURIComponent(query)}` : "/search/");
      }
      if (frontendOnly) event.preventDefault();
    }
    document.addEventListener("submit", submit);
    document.addEventListener("click", click);
    document.addEventListener("keydown", key);
    document.addEventListener("input", input);
    layout();
    return () => {
      document.removeEventListener("submit", submit);
      observer.disconnect();
      cancelAnimationFrame(frame);
      window.removeEventListener("resize", schedule);
      document.removeEventListener("click", click);
      document.removeEventListener("keydown", key);
      document.removeEventListener("input", input);
    };
  });
</script>

<svelte:head>
  <title>{title}</title>
  <meta
    name="description"
    content="The Sustainabilist — sustainability news, interviews and insights from the UAE and beyond."
  />
  {#each homepage.styles as stylesheet}<link
      rel="stylesheet"
      href={stylesheet}
    />{/each}
  <link rel="stylesheet" href="/replica.css" />
</svelte:head>

{@html body}
