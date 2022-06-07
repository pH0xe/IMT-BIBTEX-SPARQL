<script setup lang="ts">
import AppHeader from "./components/AppHeader.vue";
</script>

<template>
	<div class="main">
		<AppHeader />
		<router-view />
	</div>
</template>

<style>
@import "bulma/css/bulma.css";
@import "@mdi/font/css/materialdesignicons.css";

#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	color: #2c3e50;
}
.main {
	height: 100vh;
	display: flex;
	flex-direction: column;
}
router-view {
	flex-grow: 1;
}
</style>
