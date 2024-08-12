<script>
	let message = 'Loading...';

	async function fetchMessage() {
		try {
			const response = await fetch('http://localhost:5000/api/message');
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
