<script lang="ts">
  import Replica from "$lib/Replica.svelte";
  import editorialCalendar from "$lib/editorial-calendar.json";

  export let month: string;
  export let topic: string;
  export let image: string;

  const pageStart = editorialCalendar.body.indexOf('<div class="page-wrap">');
  const footerStart = editorialCalendar.body.indexOf(
    '<div class="sustainabilist-footer">',
  );
  $: detailBody = `<div class="page-wrap"><label for="menu-switch" id="menu-toggle"></label><div class="container" role="main"><div class="page-header"><div class="header-inr"><h1>${topic}</h1></div></div><section class="mbr-section"><div class="holder"><div class="safaqat-inner"><div class="what-we-do"></div></div></div></section></div></div>`;
  $: homepage = {
    ...editorialCalendar,
    body:
      editorialCalendar.body.slice(0, pageStart) +
      detailBody +
      editorialCalendar.body.slice(footerStart),
  };
</script>

<Replica {homepage} title={`${topic} | The Sustainabilist`} frontendOnly />
