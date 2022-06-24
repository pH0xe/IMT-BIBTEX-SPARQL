<script setup lang="ts">
import { ref } from "vue";

const toggle: any = ref(true);
</script>

<template>
	<header>
		<nav v-if="toggle" class="navbar is-primary">
			<div class="navbar-brand">
				<div class="navbar-item mr-5">
					<span class="icon is-large mb-1">
						<i class="mdi mdi-script-text mdi-36px" />
					</span>
					<h1 class="title has-text-white">
						Bibtex parser
					</h1>
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
						<span>{{ $t("Files") }}</span>
					</span>
				</router-link>
				<router-link to="account" class="navbar-item">
					<span class="icon-text">
						<span class="icon">
							<i class="mdi mdi-24px mdi-account" />
						</span>
						<span>{{ $t("Accounts") }}</span>
					</span>
				</router-link>
				<router-link to="help" class="navbar-item">
					<span class="icon-text">
						<span class="icon">
							<i class="mdi mdi-24px mdi-help" />
						</span>
						<span>{{ $t("Help") }}</span>
					</span>
				</router-link>
			</div>
		</nav>
	</header>
</template>
