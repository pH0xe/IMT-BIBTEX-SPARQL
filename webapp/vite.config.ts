import { fileURLToPath, URL } from 'url';

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import checker from 'vite-plugin-checker';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		vue(),
		checker({
			typescript: true,
			vueTsc: true,
			eslint: { lintCommand: 'eslint --ext .ts,.vue src' },
		}),
	],
	resolve: {
		alias: {
			"@": fileURLToPath(new URL("./src", import.meta.url)),
		},
	},
	server: {
		port: 8080,
	},
});
