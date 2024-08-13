// frontend/src/routes/api/message/+server.ts

import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async () => {
	const response = await fetch('http://localhost:5000/api/message');
	const data = await response.json();
	return json(data);
};
