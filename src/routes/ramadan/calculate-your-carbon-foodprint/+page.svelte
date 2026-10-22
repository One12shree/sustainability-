<script>
  import Replica from "$lib/Replica.svelte";
  import homepage from "$lib/calculate-your-carbon-foodprint.json";
</script>

<Replica
  {homepage}
  title="Carbon FoodPrint Calculator | The Sustainabilist"
  frontendOnly
/>
