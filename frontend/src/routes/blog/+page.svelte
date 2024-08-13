<!-- frontend/src/routes/blog/+page.svelte -->

<script>
	export let data;
	const { posts } = data;
</script>

<h1>Blog</h1>

<h3>
	<a href="/blog/category">View all categories</a>
</h3>

{#if posts.length}
	<ul>
		{#each posts as post}
			<li>
				<a data-sveltekit:prefetch href={`/blog/${post.path}`}>{post.meta.title}</a>
				<p>Published: {new Date(post.meta.date).toLocaleDateString()}</p>
				{#if post.meta.categories && post.meta.categories.length}
					<p>
						Categories:
						{#each post.meta.categories as category, index}
							<a href={`/blog/category/${category}`}>{category}</a
							>{#if index < post.meta.categories.length - 1},
							{/if}
						{/each}
					</p>
				{/if}
			</li>
		{/each}
	</ul>
{:else}
	<p>No posts found.</p>
{/if}
