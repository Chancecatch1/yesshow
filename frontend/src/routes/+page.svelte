<!-- frontend/src/routes/+page.svelte -->

<script>
	let message = 'Loading...';

	async function fetchMessage() {
		try {
			// import.meta.env로 환경 변수를 가져옵니다.
			const response = await fetch(`${import.meta.env.VITE_API_URL}/api/message`);
			const data = await response.json();
			message = data.message;
		} catch (error) {
			message = 'Error fetching message';
			console.error('Error:', error);
		}
	}

	fetchMessage();
</script>

<main>
	<h1>{message}</h1>
</main>
