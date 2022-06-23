<script setup lang="ts">
import axios from "axios";
import { computed, ComputedRef, ref, Ref } from "vue";

const emit = defineEmits(["invalidToken"])
const { token } = defineProps<{ token: string }>();

const API_HOST = "localhost";
const API_PORT = "5000";

const EMPTY_PASSWORD_MESSAGE = "Password must not be empty.";
const INVALID_PASSWORD_MESSAGE = "Invalid password";
const NETWORK_ERROR_MESSAGE = "Unable to reach server. Please check your connection.";
const UNEQUAL_PASSWORD = "Entered password are not equal";

const passwordUpdated: Ref<boolean> = ref(false);

const isUpdatingPassword: Ref<boolean> = ref(false);

const currentPassword: Ref<string> = ref("");
const newPassword: Ref<string> = ref("");
const confirmNewPassword: Ref<string> = ref("");

const errorMessage: Ref<string | undefined> = ref(undefined);
const hasError: ComputedRef<boolean> = computed(() => errorMessage.value !== undefined);

function clearError(): void {
	errorMessage.value = undefined;
}

function startPasswordUpdate(): void {
	isUpdatingPassword.value = true;
	currentPassword.value = "";
	newPassword.value = "";
	confirmNewPassword.value = "";
	passwordUpdated.value = false;
}

function stopPasswordUpdate(): void {
	isUpdatingPassword.value = false;
}

async function updatePassword(): Promise<void> {
	clearError();

	if (newPassword.value !== confirmNewPassword.value) {
		errorMessage.value = UNEQUAL_PASSWORD;
	} else if (newPassword.value.length === 0) {
		errorMessage.value = EMPTY_PASSWORD_MESSAGE;
		return;
	}

	await axios.put(
		`http://${API_HOST}:${API_PORT}/api/auth/password`,
		{
			currentPassword: currentPassword.value,
			newPassword: newPassword.value,
		},
		{
			headers: {
				"Content-Type": "multipart/form-data",
				Authorization: token,
			},
		}
	)
		.then(() => {
			stopPasswordUpdate();
			passwordUpdated.value = true;
		})
		.catch((error) => {
			if (error.response.status === 401) {
				emit("invalidToken");
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
}
</script>

<template>
	<div v-if="!isUpdatingPassword" class="has-text-centered">
		<button @click="startPasswordUpdate" class="button is-primary">
			<span class="icon-text">
				<span class="icon">
					<i class="mdi mdi-24px mdi-pencil" />
				</span>
				<span>Change password</span>
			</span>
		</button>
		<p v-if="passwordUpdated" class="has-text-success">
			<span class="icon-text">
				<span class="icon">
					<i class="mdi mdi-check" />
				</span>
				<span class="is-size-7">Password successfully updated</span>
			</span>
		</p>
	</div>
	<form name="New password" v-else>
		<div v-if="hasError" class="notification is-danger">
			<p>
				{{ errorMessage }}
			</p>
		</div>
		<h2 class="title is-5">Change password</h2>
		<div class="field">
			<label class="label" for="current-password">Current password</label>
			<div class="control has-icons-left">
				<input v-model="currentPassword" id="current-password" class="input" type="password" placeholder="Current password">
				<span class="icon is-left">
					<i class="mdi mdi-key-variant"></i>
				</span>
			</div>
		</div>
		<div class="field">
			<label class="label" for="new-password">Password</label>
			<div class="control has-icons-left">
				<input v-model="newPassword" id="new-password" class="input" type="password" autocomplete="new-password" placeholder="Password">
				<span class="icon is-left">
					<i class="mdi mdi-key-variant"></i>
				</span>
			</div>
		</div>
		<div class="field">
			<label class="label" for="new-password-confirm">Confirm password</label>
			<div class="control has-icons-left">
				<input v-model="confirmNewPassword" id="new-password-confirm" class="input" type="password" autocomplete="new-password" placeholder="Confirm password">
				<span class="icon is-left">
					<i class="mdi mdi-key-variant"></i>
				</span>
			</div>
		</div>
		<div class="field has-text-centered">
			<button @click="stopPasswordUpdate" class="button is-ghost has-text-danger">
				<span class="icon-text">
					<span class="icon">
						<i class="mdi mdi-24px mdi-cancel" />
					</span>
					<span>Cancel</span>
				</span>
			</button>
			<button @click="updatePassword" type="button" class="button is-primary">
				<span class="icon-text">
					<span class="icon">
						<i class="mdi mdi-24px mdi-check" />
					</span>
					<span>Confirm</span>
				</span>
			</button>
		</div>
	</form>
</template>
