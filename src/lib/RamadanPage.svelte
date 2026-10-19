<script>
	export let kind = 'guide';
	let food = 'Tomato';
	let frequency = '1-2 a week';
	const foods = { Tomato: 34, Beans: 22, Chicken: 96, Beef: 390, Rice: 58, Tofu: 18 };
	const frequencies = { '1-2 a week': 1, '3-5 a week': 2.4, 'Once a day': 4, '2 a day': 8 };
	$: footprint = Math.round(foods[food] * frequencies[frequency]);
</script>

<svelte:head><title>{kind === 'guide' ? 'Low Carbon Cooking' : kind === 'calculator' ? 'Carbon FoodPrint Calculator' : kind === 'recipes' ? 'Low Carbon Recipes' : 'Low Carbon Cooking Partners'} | The Sustainabilist</title></svelte:head>

<main>
	<header><a class="brand" href="/ramadan/">THE SUSTAINABILIST</a><a href="/ramadan/">← Ramadan hub</a></header>
	{#if kind === 'guide'}
		<section class="original-article">
			<h1>The Keys to Eating a Low Carbon Diet</h1>
			<p>Food production is responsible for around 1/3 of worldwide greenhouse gas emissions. Transitioning to a low carbon diet can have an impact in reducing worldwide emissions and here are the key changes you need to make to get started.</p>
			<h2>Reduce Your Meat Consumption</h2>
			<p>Reducing or cutting meat from your diet will have the most emphatic impact on your diet. Considering the energy and water required in the meat value chain, a significant amount of GHG emissions is reduced when opting out of meat consumption.</p>
			<h2>Be Afraid of Freight</h2>
			<p>While importing food from overseas adds to its carbon footprint, the importing of foods is not as important as how they are brought in. If it’s possible, eat as locally as you can, and if you can’t eat local, find out how your food is imported to see if it’s an efficient mode of shipment.</p>
			<h2>A More Seasonal Approach</h2>
			<p>Eat foods that are in season. This means you don’t just get the most environmentally friendly produce, but produce that’s high in nutrition and tastes better too.</p>
			<h2>Don’t Fail to Plan</h2>
			<p>Around 19% of purchased food is wasted after it makes it to homes and restaurants. Reducing food waste therefore becomes imperative to reduce carbon emissions and reduce emissions from excess food production and waste management.</p>
			<img src="/assets/page-ca8a51536559-1-2.jpg" alt="Low-carbon food on a table" />
		</section>
	{:else if kind === 'calculator'}
		<section class="hero calculator"><p class="eyebrow">RAMADAN TOOL</p><h1>What’s your diet’s carbon footprint?</h1><p>Choose an ingredient and how often you eat it for an illustrative annual estimate.</p></section>
		<section class="content"><div class="controls"><label>Which food would you like?<select bind:value={food}>{#each Object.keys(foods) as option}<option>{option}</option>{/each}</select></label><label>How often do you have it?<select bind:value={frequency}>{#each Object.keys(frequencies) as option}<option>{option}</option>{/each}</select></label></div><div class="result"><p class="eyebrow">YOUR ESTIMATE</p><h2>{footprint} kg CO₂e per year</h2><p>Your {food.toLowerCase()} consumption is estimated to contribute <strong>{footprint} kg</strong> to annual greenhouse-gas emissions.</p><p><strong>{Math.round(footprint * 4.2)} km</strong> of equivalent regular petrol-car travel.</p><small>This educational tool provides broad estimates, not a personalised footprint assessment.</small></div></section>
	{:else if kind === 'recipes'}
		<section class="hero recipes"><p class="eyebrow">RAMADAN RECIPES</p><h1>Low-carbon cooking for Iftar</h1><p>Simple, generous meals with vegetables, grains and pulses at their heart.</p></section>
		<section class="content"><div class="grid"><article><h2>Roasted vegetable &amp; chickpea traybake</h2><p>Seasonal vegetables, chickpeas, herbs and tahini make an easy shared Iftar dish.</p></article><article><h2>Red lentil soup</h2><p>A warming staple using red lentils, tomatoes, cumin and a squeeze of lemon.</p></article><article><h2>Herbed rice with beans</h2><p>Use leftover rice with beans, greens and fragrant herbs for a quick, filling meal.</p></article><article><h2>Date &amp; oat energy bites</h2><p>Dates, oats and nuts create a naturally sweet bite for breaking the fast.</p></article></div></section>
	{:else}
		<section class="hero partners"><p class="eyebrow">COOK TOGETHER</p><h1>Low-carbon cooking partners</h1><p>Progress happens when households, food makers and communities take part together.</p></section>
		<section class="content center"><h2>Be part of the conversation</h2><p>We welcome organisations that make it easier to choose seasonal, local and plant-forward food. Share resources, recipes and ideas that help communities waste less and enjoy more.</p><p><a class="button" href="/ramadan/how-to-eat-low-carbon/">Explore the guide</a> <a class="button" href="/ramadan/recipes/">Browse recipes</a></p></section>
	{/if}
</main>

<style>
	:global(*){box-sizing:border-box}:global(body){margin:0;font-family:Arial,sans-serif;color:#17231a;background:#fcfcf7}header{height:76px;max-width:1160px;padding:0 28px;margin:auto;display:flex;justify-content:space-between;align-items:center}header a{color:#386e3c;font-weight:700;text-decoration:none}.brand{color:#17231a!important;letter-spacing:1.5px}.hero{min-height:370px;display:grid;place-content:center;text-align:center;padding:55px 25px;color:white;background:#274e33 center/cover;background-blend-mode:multiply}.calculator{background-image:url('/assets/page-44954e5e792c-2-2.jpg')}.recipes{background-image:url('/assets/page-07bda5b54e72-3-2.jpg')}.partners{background-image:url('/assets/page-cce4941c2834-4-1.jpg')}h1{font:400 clamp(2.5rem,6vw,4.8rem)/1.05 Georgia,serif;max-width:860px;margin:8px auto 16px}h2{font:400 1.55rem/1.2 Georgia,serif}.eyebrow{font-size:.75rem;font-weight:800;letter-spacing:2px}.original-article{max-width:940px;margin:50px auto 80px;padding:10px 28px 0}.original-article h1{font-size:43px;text-align:center;color:#000;margin:25px auto 40px}.original-article h2{font-size:26px;color:#000;margin:35px 0 12px}.original-article p{font-size:17px;line-height:1.7;color:#222;margin:0}.original-article img{display:block;width:100%;max-width:809px;margin:45px auto 0}.content{max-width:1050px;margin:auto;padding:72px 28px}.intro{max-width:760px;margin:0 auto 38px;text-align:center;font:1.25rem/1.65 Georgia,serif}.grid,.controls{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}article,.result{background:#edf4e8;padding:30px}article p,.center p,.result p{line-height:1.6}.controls{margin-bottom:25px}label{display:grid;gap:8px;font-weight:bold}select{padding:15px;font-size:1rem;border:1px solid #799379;background:white}.result{text-align:center;background:#dcebd4;padding:44px}.result h2{font-size:2.4rem}.center{max-width:720px;text-align:center}.button{display:inline-block;background:#315d36;color:white;padding:14px 20px;margin:5px;text-decoration:none;font-weight:bold}@media(max-width:650px){header{height:64px;padding:0 18px}.brand{font-size:.75rem}.original-article{margin-top:25px;padding:0 20px}.original-article h1{font-size:32px;margin-bottom:28px}.original-article h2{font-size:23px}.grid,.controls{grid-template-columns:1fr}.content{padding:45px 20px}.result{padding:28px 18px}}
</style>
