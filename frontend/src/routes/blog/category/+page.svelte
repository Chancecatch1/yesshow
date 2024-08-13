<script>
	export let data;
	const { uniqueCategories } = data;
</script>

<h1>All blog categories</h1>

<ul>
	{#each uniqueCategories as category}
		<li>
			<a href="/blog/category/{category.title}">{category.title}</a>
			({category.count})
		</li>
	{/each}
</ul>
