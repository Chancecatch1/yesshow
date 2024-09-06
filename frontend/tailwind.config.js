// frontend/tailwind.config.js

/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			fontFamily: {
				'noto-sans-kr': ['Noto Sans KR', 'sans-serif']
			},
			colors: {
				'graph-blue': 'steelblue',
				'graph-red': 'red',
				'graph-green': 'green'
			},
			height: {
				graph: '400px'
			}
		}
	},
	plugins: []
};
