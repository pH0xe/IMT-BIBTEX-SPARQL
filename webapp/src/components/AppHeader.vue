<script setup lang="ts">
import { ref } from "vue";

const toggle: any = ref(true);
</script>

<template>
	<header>
		<nav class="navbar is-primary" v-if="toggle">
			<div class="navbar-brand">
				<div class="navbar-item">
					<h1 class="title has-text-white">Bibtex to RDF</h1>
				</div>
				<router-link to="sparklis" class="navbar-item">
					<span class="icon-text">
						<span class="icon">
							<i class="mdi mdi-24px mdi-magnify" />
						</span>
						<span>Sparklis</span>
					</span>
				</router-link>
				<router-link to="files" class="navbar-item">
					<span class="icon-text">
						<span class="icon">
							<i class="mdi mdi-24px mdi-file" />
						</span>
						<span>Files</span>
					</span>
				</router-link>
			</div>
		</nav>
	</header>
</template>
