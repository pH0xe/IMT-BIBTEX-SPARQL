import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		name: "not-found",
		path: "/:pathMatch(.*)*",
		redirect: "sparklis",
	}, {
		name: "files",
		path: "/files",
		component: () => import("@/components/FileManager.vue"),
	}, {
		name: "sparklis",
		path: "/sparklis",
		component: () => import("@/components/SparklisViewer.vue"),
	}, {
		name: "account",
		path: "/account",
		component: () => import("@/components/AccountManager.vue"),
	},
];

export default createRouter({
	history: createWebHistory(),
	routes,
});
