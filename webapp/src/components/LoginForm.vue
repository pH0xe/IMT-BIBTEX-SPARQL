<script setup lang="ts">
import axios from "axios";
import { computed, ComputedRef, ref, Ref } from "vue";

const emit = defineEmits(["loggedIn"]);

const API_HOST = "localhost";
const API_PORT = "5000";

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
		<h2 class="title is-5 has-text-centered">Authentification</h2>

		<form name="login">
			<div v-if="hasError" class="notification is-danger is-light">
				<p>
					{{ errorMessage }}
				</p>
			</div>
			<div class="field">
				<label class="label">Login</label>
				<div class="control has-icons-left">
					<input v-model="login" class="input" type="text" placeholder="Login">
					<span class="icon is-left">
						<i class="mdi mdi-identifier"></i>
					</span>
				</div>
			</div>
			<div class="field">
				<label class="label">Password</label>
				<div class="control has-icons-left">
					<input v-model="password" class="input" type="password" placeholder="Password">
					<span class="icon is-left">
						<i class="mdi mdi-key-variant"></i>
					</span>
				</div>
			</div>
			<div class="field">
				<div class="control has-text-centered">
					<button @click="connect" type="button" class="button is-primary">
						<span class="icon-text">
							<span class="icon">
								<i class="mdi mdi-24px mdi-login-variant" />
							</span>
							<span>Log in</span>
						</span>
					</button>
				</div>
			</div>
		</form>
	</section>
</template>
