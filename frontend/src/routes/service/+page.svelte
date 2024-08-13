<!-- frontend/src/routes/service/+page.svelte -->

<script lang="ts">
	import { onMount } from 'svelte';

	let message: string = '';

	onMount(async () => {
		const response = await fetch('/api/posts');
		if (response.ok) {
			message = await response.text();
		} else {
			message = 'Failed to load data';
		}
	});
</script>

<main class="w-full max-w-[850px] mx-auto p-4 relative">
	<h1 class="text-2xl font-bold mb-4">Service Page</h1>
	<p class="text-lg text-gray-700">{message}</p>
</main>
