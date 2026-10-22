<script>
  import Replica from "$lib/Replica.svelte";
  import homepage from "$lib/trending-articles.json";
</script>

<Replica
  {homepage}
  title="Trending Articles | The Sustainabilist"
  frontendOnly
/>
