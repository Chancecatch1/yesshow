<!-- frontend/src/routes/blog/category/[category]/+page.svelte -->

<script>
	export let data;
	const { category, posts } = data;
</script>

<h1>Blog category: {category}</h1>

{#if posts.length}
	<aside>
		<h2>Posted in:</h2>
		<ul>
			{#each posts as post}
				<li>
					<a href={post.path}>
						{post.meta.title}
					</a>
				</li>
			{/each}
		</ul>
	</aside>
{/if}
