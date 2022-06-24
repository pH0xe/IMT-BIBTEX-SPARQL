<script setup lang="ts">
import axios from "axios";
import { computed, ComputedRef, ref, Ref } from "vue";

const emit = defineEmits(["loggedIn"]);

const API_HOST = import.meta.env.API_HOST;
const API_PORT = import.meta.env.API_PORT;

const INVALID_LOGIN_OR_PASSWORD_MESSAGE = "Invalid login or password.";
const NETWORK_ERROR_MESSAGE = "Unable to reach server. Please check your connection.";

const login: Ref<string> = ref(sessionStorage.getItem("login") || "");
const password: Ref<string> = ref("");

const errorMessage: Ref<string | undefined> = ref(undefined);
const hasError: ComputedRef<boolean> = computed(() => errorMessage.value !== undefined);

function clearError(): void {
	errorMessage.value = undefined;
}

async function connect(): Promise<void> {
	await axios.post(
		`http://${API_HOST}:${API_PORT}/api/auth/login`,
		{
			login: login.value,
			password: password.value,
		}, {
			headers: { "Content-Type": "multipart/form-data" },
		}
	)
		.then((response) => {
			clearError();

			sessionStorage.setItem("token", response.data.token);
			sessionStorage.setItem("login", login.value);

			emit("loggedIn");
		})
		.catch((error) => {
			if (error.response.status == 401) {
				errorMessage.value = INVALID_LOGIN_OR_PASSWORD_MESSAGE;
				password.value = "";
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
}
</script>

<template>
	<section class="section">
		<h2 class="title is-5 has-text-centered">
			{{ $t("Authentification") }}
		</h2>

		<form name="login">
			<div v-if="hasError" class="notification is-danger is-light">
				<p>
					{{ $t(errorMessage) }}
				</p>
			</div>
			<div class="field">
				<label class="label">{{ $t("Login") }}</label>
				<div class="control has-icons-left">
					<input v-model="login" class="input" type="text" :placeholder="$t('Login')">
					<span class="icon is-left">
						<i class="mdi mdi-identifier" />
					</span>
				</div>
			</div>
			<div class="field">
				<label class="label">{{ $t("Password") }}</label>
				<div class="control has-icons-left">
					<input v-model="password" class="input" type="password" :placeholder="$t('Password')">
					<span class="icon is-left">
						<i class="mdi mdi-key-variant" />
					</span>
				</div>
			</div>
			<div class="field">
				<div class="control has-text-centered">
					<button class="button is-primary" type="button" @click="connect">
						<span class="icon-text">
							<span class="icon">
								<i class="mdi mdi-24px mdi-login-variant" />
							</span>
							<span>{{ $t("Log in") }}</span>
						</span>
					</button>
				</div>
			</div>
		</form>
	</section>
</template>
