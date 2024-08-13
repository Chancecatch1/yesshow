import { json } from '@sveltejs/kit';
import { comments } from '$lib/comment';

export function GET(requestEvent) {
	const { params } = requestEvent;
	const { commentId } = params;

	const comment = comments.find((comment) => comment.id === parseInt(commentId));

	return json(comment);
}

export async function PATCH(requestEvent) {
	const { params, request } = requestEvent;
	const { commentId } = params;
	const { text } = await request.json();

	const findedComment = comments.find((comment) => comment.id === parseInt(commentId));
	findedComment.text = text;

	return json(findedComment);
}

export async function DELETE(requestEvent) {
	const { params } = requestEvent;
	const { commentId } = params;

	const deletedComment = comments.find((comment) => comment.id === parseInt(commentId));
	const index = comments.findIndex((comment) => comment.id === parseInt(commentId));

	comments.splice(index, 1);

	return json(deletedComment);
}
