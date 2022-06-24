<script setup lang="ts">
import axios from "axios";
import { computed, ComputedRef, ref, Ref } from "vue";

const emit = defineEmits(["invalidToken", "newUser"]);
const props = defineProps<{ token: string }>();

const API_HOST = "localhost";
const API_PORT = 5000;

const EMPTY_PASSWORD_MESSAGE = "Password must not be empty.";
const NETWORK_ERROR_MESSAGE = "Unable to reach server. Please check your connection.";
const UNAVAILABLE_LOGIN_MESSAGE = "This login is not available";
const UNEQUAL_PASSWORD = "Entered password are not equal";

const isAddingUser: Ref<boolean> = ref(false);
const login: Ref<string> = ref("");
const password: Ref<string> = ref("");
const confirmPassword: Ref<string> = ref("");

const errorMessage: Ref<string | undefined> = ref(undefined);
const hasError: ComputedRef<boolean> = computed(() => errorMessage.value !== undefined);

function clearError(): void {
	errorMessage.value = undefined;
}

function startUserCreation(): void {
	isAddingUser.value = true;
	login.value = "";
	password.value = "";
	confirmPassword.value = "";
}

function cancelUserCreation(): void {
	isAddingUser.value = false;
}

async function postNewUser(): Promise<void> {
	clearError();

	if (password.value !== confirmPassword.value) {
		errorMessage.value = UNEQUAL_PASSWORD;
	} else if (password.value.length === 0) {
		errorMessage.value = EMPTY_PASSWORD_MESSAGE;
		return;
	}

	await axios.post(
		`http://${API_HOST}:${API_PORT}/api/auth/register`,
		{
			login: login.value,
			password: password.value,
		}, {
			headers: {
				"Content-Type": "multipart/form-data",
				Authorization: props.token || "",
			},
		}
	)
		.then(() => {
			emit("newUser");
			isAddingUser.value = false;
		})
		.catch((error) => {
			if (error.response.status === 401) {
				emit("invalidToken");
			} else if (error.response.status === 400) {
				errorMessage.value = UNAVAILABLE_LOGIN_MESSAGE;
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
}
</script>

<template>
	<div v-if="hasError" class="notification is-danger">
		<p>
			{{ $t(errorMessage) }}
		</p>
	</div>
	<form v-if="isAddingUser" :name="$t('New user')">
		<h2 class="title is-5">
			{{ $t("New user") }}
		</h2>
		<div class="field">
			<label class="label" for="new-user-login">{{ $t("Login") }}</label>
			<div class="control has-icons-left">
				<input
					id="new-user-login"
					v-model="login"
					class="input"
					autocomplete="username"
					:placeholder="$t('Login')"
				>
				<span class="icon is-left">
					<i class="mdi mdi-identifier" />
				</span>
			</div>
		</div>
		<div class="field">
			<label class="label" for="new-user-password">{{ $t("Password") }}</label>
			<div class="control has-icons-left">
				<input
					id="new-user-password"
					v-model="password"
					class="input"
					type="password"
					autocomplete="new-password"
					:placeholder="$t('Password')"
				>
				<span class="icon is-left">
					<i class="mdi mdi-key-variant" />
				</span>
			</div>
		</div>
		<div class="field">
			<label class="label" for="new-user-password">{{ $t("Confirm password") }}</label>
			<div class="control has-icons-left">
				<input
					id="new-user-password"
					v-model="confirmPassword"
					class="input"
					type="password"
					autocomplete="new-password"
					:placeholder="$t('Confirm password')"
				>
				<span class="icon is-left">
					<i class="mdi mdi-key-variant" />
				</span>
			</div>
		</div>
		<div class="field has-text-centered">
			<button class="button is-ghost has-text-danger" @click="cancelUserCreation">
				<span class="icon-text">
					<span class="icon">
						<i class="mdi mdi-24px mdi-cancel" />
					</span>
					<span>{{ $t("Cancel") }}</span>
				</span>
			</button>
			<button class="button is-primary" type="button" @click="postNewUser">
				<span class="icon-text">
					<span class="icon">
						<i class="mdi mdi-24px mdi-check" />
					</span>
					<span>{{ $t("Confirm") }}</span>
				</span>
			</button>
		</div>
	</form>
	<div v-else class="has-text-centered">
		<button class="button is-primary" @click="startUserCreation">
			<span class="icon-text">
				<span class="icon">
					<i class="mdi mdi-24px mdi-plus-circle" />
				</span>
				<span>{{ $t("Add user") }}</span>
			</span>
		</button>
	</div>
</template>

