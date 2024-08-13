<!-- frontend/src/routes/service/+page.svelte -->

<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	let isOpen = writable(false);
	function toggleMenu() {
		isOpen.update((n) => !n);
	}

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

	<div class="relative inline-block text-left">
		<!-- 타이틀과 드롭다운을 포함한 상위 요소 -->
		<div class="flex items-center gap-4">
			<!-- 타이틀 -->
			<span class="text-lg font-semibold text-gray-900">Dropdown Title</span>

			<!-- 드롭다운 버튼 -->
			<div>
				<button
					on:click={toggleMenu}
					type="button"
					class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
					id="menu-button"
					aria-expanded="true"
					aria-haspopup="true"
				>
					Options
					<svg
						class="-mr-1 h-5 w-5 text-gray-400"
						viewBox="0 0 20 20"
						fill="currentColor"
						aria-hidden="true"
					>
						<path
							fill-rule="evenodd"
							d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
							clip-rule="evenodd"
						/>
					</svg>
				</button>
			</div>
		</div>

		<!-- 드롭다운 메뉴 -->
		{#if $isOpen}
			<div
				class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
				role="menu"
				aria-orientation="vertical"
				aria-labelledby="menu-button"
				tabindex="-1"
			>
				<div class="py-1" role="none">
					<a
						href="#"
						class="block px-4 py-2 text-sm text-gray-700"
						role="menuitem"
						tabindex="-1"
						id="menu-item-0">Account settings</a
					>
					<a
						href="#"
						class="block px-4 py-2 text-sm text-gray-700"
						role="menuitem"
						tabindex="-1"
						id="menu-item-1">Support</a
					>
					<a
						href="#"
						class="block px-4 py-2 text-sm text-gray-700"
						role="menuitem"
						tabindex="-1"
						id="menu-item-2">License</a
					>
					<form method="POST" action="#" role="none">
						<button
							type="submit"
							class="block w-full px-4 py-2 text-left text-sm text-gray-700"
							role="menuitem"
							tabindex="-1"
							id="menu-item-3">Sign out</button
						>
					</form>
				</div>
			</div>
		{/if}
	</div>
</main>
