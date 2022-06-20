<script setup lang="ts">
import AppHeader from "./components/AppHeader.vue";
</script>

<template>
	<div class="container">
		<AppHeader />
		<router-view />
	</div>
</template>

<style>
/* @import "bulma/css/bulma.css"; */

#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
}
.container {
	height: 100vh;
	display: flex;
	flex-direction: column;
}
router-view {
	flex-grow: 1;
}
</style>
