export const load = async ({ fetch }) => {
	const response = await fetch(`/api/posts`);
	const posts = await response.json();

	let uniqueCategories = {};

	posts.forEach((post) => {
		if (post.meta.categories) {
			post.meta.categories.forEach((category) => {
				if (uniqueCategories.hasOwnProperty(category)) {
					uniqueCategories[category].count += 1;
				} else {
					uniqueCategories[category] = {
						title: category,
						count: 1
					};
				}
			});
		}
	});

	const sortedUniqueCategories = Object.values(uniqueCategories).sort((a, b) =>
		a.title.localeCompare(b.title)
	);

	return {
		uniqueCategories: sortedUniqueCategories
	};
};
