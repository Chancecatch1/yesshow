// frontend/src/routes/api/posts/+server.ts

import { fetchMarkdownPosts } from '$lib/utils';
import { json } from '@sveltejs/kit';

export const GET = async () => {
	const allPosts = await fetchMarkdownPosts();

	const sortedPosts = allPosts
		.map((post) => ({
			...post,
			meta: {
				...post.meta,
				categories: post.meta.categories || []
			}
		}))
		.sort((a, b) => {
			return new Date(b.meta.date) - new Date(a.meta.date);
		});

	return json(sortedPosts);
};
