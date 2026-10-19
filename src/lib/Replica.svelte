<script lang="ts">
	import { onMount } from 'svelte';
	import initialHomepage from '$lib/homepage.json';
	export let homepage = initialHomepage;
	export let title = 'The Sustainabilist';
	export let frontendOnly = false;
	const ramadanLinks: Record<string, string> = {
		'https://thesustainabilist.ae/how-to-eat-low-carbon/': '/ramadan/how-to-eat-low-carbon/',
		'https://thesustainabilist.ae/calculate-your-carbon-foodprint/': '/ramadan/calculate-your-carbon-foodprint/',
		'https://thesustainabilist.ae/recipe/': '/ramadan/recipes/',
		'https://thesustainabilist.ae/low-carbon-cooking-partners/': '/ramadan/low-carbon-cooking-partners/'
	};
	$: body = Object.entries(ramadanLinks).reduce((html, [from, to]) => html.replaceAll(from, to), homepage.body);

	onMount(() => {
		const grid = document.querySelector<HTMLElement>('#grid');
		let frame = 0;
		function layout() {
			if (!grid) return;
			const columns = window.innerWidth <= 600 ? 1 : window.innerWidth <= 900 ? 2 : 3;
			grid.classList.add('masonry');
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
		function schedule() { cancelAnimationFrame(frame); frame = requestAnimationFrame(layout); }
		const observer = new ResizeObserver(schedule);
		if (grid) for (const card of grid.children) observer.observe(card);
		window.addEventListener('resize', schedule);
		function click(event: MouseEvent) {
			const target = event.target instanceof Element ? event.target : null;
			if (target?.closest('.home-subs')) {
				event.preventDefault();
				const popup = document.querySelector<HTMLElement>('.popup');
				if (popup) { popup.style.display = 'block'; popup.setAttribute('role', 'dialog'); popup.setAttribute('aria-label', 'Subscribe to The Sustainabilist'); popup.querySelector<HTMLInputElement>('input[type=email]')?.focus(); }
			}
			if (target?.closest('.close')) { event.preventDefault(); document.querySelectorAll<HTMLElement>('.popup').forEach(p => p.style.display = 'none'); }
			if (target?.closest('.ram')) {
                const panel = document.querySelector<HTMLElement>('.cntram');
                if (panel) panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
            }
            if (target?.closest('.collapsible')) {
                const button = target.closest('.collapsible');
                const panel = button?.nextElementSibling as HTMLElement | null;
                if (panel) { const open = button?.getAttribute('aria-expanded') === 'true'; button?.setAttribute('aria-expanded', String(!open)); panel.style.maxHeight = open ? '0px' : `${panel.scrollHeight}px`; panel.style.overflow = 'hidden'; }
            }
            if (target?.closest('.promagnifier')) document.querySelector<HTMLFormElement>('.proinput form')?.requestSubmit();
		}
		function key(event: KeyboardEvent) {
			if (event.key === 'Escape') { document.querySelectorAll<HTMLElement>('.popup').forEach(p => p.style.display = 'none'); const menu = document.querySelector<HTMLInputElement>('#menu-switch'); if (menu) menu.checked = false; }
		}
		function submit(event: SubmitEvent) { if (frontendOnly) event.preventDefault(); }
        document.addEventListener('submit', submit);
        document.addEventListener('click', click);
		document.addEventListener('keydown', key);
		layout();
		return () => { document.removeEventListener('submit', submit); observer.disconnect(); cancelAnimationFrame(frame); window.removeEventListener('resize', schedule); document.removeEventListener('click', click); document.removeEventListener('keydown', key); };
	});
</script>

<svelte:head>
	<title>{title}</title>
	<meta name="description" content="The Sustainabilist — sustainability news, interviews and insights from the UAE and beyond." />
	{#each homepage.styles as stylesheet}<link rel="stylesheet" href={stylesheet} />{/each}
	<link rel="stylesheet" href="/replica.css" />
</svelte:head>

{@html body}
