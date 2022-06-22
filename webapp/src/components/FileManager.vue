<script setup lang="ts">
import axios from "axios";
import { computed, ComputedRef, ref, Ref, watch } from "vue";

const API_HOST = "localhost";
const API_PORT = "5000";

const INVALID_PASSWORD_MESSAGE = "Invalid login or password.";
const NETWORK_ERROR_MESSAGE = "Unable to reach server. Please check your connection.";

const login: Ref<string> = ref("");
const password: Ref<string> = ref("");

const token: Ref<string | null> = ref(sessionStorage.getItem("token"));
const hasToken: ComputedRef<boolean> = computed(() => token.value !== null)

const errorMessage: Ref<string | undefined> = ref(undefined);
const hasError: ComputedRef<boolean> = computed(() => errorMessage.value !== undefined);

const items: Ref<any[]> = ref([]);

function clearError(): void {
	errorMessage.value = undefined;
}

function clearToken(): void {
	clearError();
	token.value = null;
}

watch(token, () => {
	if (token.value === null) {
		sessionStorage.removeItem("token");
	} else {
		sessionStorage.setItem("token", token.value);
	}
});

async function getFiles(): Promise<void> {
	items.value = [];
	await axios.get(
		`http://${API_HOST}:${API_PORT}/api/bibtex`,
		{
			headers: { Authorization: `${token.value}` },
		},
	)
		.then((response) => response.data.forEach((item: any) => items.value.unshift(item)))
		.catch((error) => {
			if (error.response.status === 403) {
				clearToken();
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
}

async function postFile(event : Event & any): Promise<void> {
	await axios.post(
		`http://${API_HOST}:${API_PORT}/api/bibtex`,
		{
			file: event.target!.files[0],
		}, {
			headers: {
				"Content-Type": "multipart/form-data",
				Authorization: `${token.value}`,
			},
		}
	)
		.then(() => getFiles())
		.catch((error) => {
			if (error.response.status === 403) {
				clearToken();
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
}

async function deleteFile(id: number): Promise<void> {
	await axios.delete(
		`http://${API_HOST}:${API_PORT}/api/bibtex/${id}`,
		{
			headers: { Authorization: `${token.value}` }
		},
	)
		.then(() => getFiles())
		.catch((error) => {
			if (error.response.status === 403) {
				clearToken();
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
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
			token.value = response.data.token;
			clearError();
			getFiles();
 		})
 		.catch((error) => {
			if (error.response.status == 400) {
				errorMessage.value = INVALID_PASSWORD_MESSAGE;
				password.value = "";
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
}

</script>

<template>
	<section v-if="!hasToken" class="section">
		<h1 class="title has-text-centered">Bibtex files history</h1>
		<h2 class="subtitle has-text-centered">Authentification</h2>

		<form name="login">

			<div v-if="hasError" class="notification is-danger is-light">
				<p>
					{{ errorMessage }}
				</p>
			</div>
			<div class="field">
				<label class="label">Login</label>
				<div class="control">
					<input v-model="login" class="input" type="text" placeholder="Login">
				</div>
			</div>
			<div class="field">
				<label class="label">Password</label>
				<div class="control">
					<input v-model="password" class="input" type="password" placeholder="Password">
				</div>
			</div>
			<div class="field">
				<div class="control">
					<button @click="connect" type="button" class="button is-primary">Log in</button>
				</div>
			</div>
		</form>
	</section>
	<section v-else class="section">
		<h1 class="title has-text-centered">Bibtex files history</h1>
		<div v-if="hasError" class="notification is-danger">
			<p>
				{{ errorMessage }}
			</p>
		</div>

		<table v-if="items.length > 0" class="table container is-striped my-6">
			<caption>Previous uploaded bibtex files</caption>
			<thead>
				<tr>
					<th>
						Name
					</th>
					<th>
						Date
					</th>
					<th />
				</tr>
			</thead>
			<tbody>
				<tr v-for="(item, i) in items" key="i">
					<td class="content-cell">
						{{ item.name }}
					</td>
					<td class="content-cell">
						{{ new Date(item.uploadDate).toLocaleString("fr") }}
					</td>
					<td>
						<button class="button is-ghost">
							<span class="icon">
								<i class="mdi mdi-24px mdi-restore" />
							</span>
						</button>
						<button @click="deleteFile(item.id)" class="button is-ghost has-text-danger">
							<span class="icon">
								<i class="mdi mdi-24px mdi-delete" />
							</span>
						</button>
					</td>
				</tr>
			</tbody>
		</table>

		<p v-else class="block is-size-4">
			No bibtex file found. Upload one to parse it.
		</p>

		<div class="has-text-centered">
			<input id="upload-button" @change="postFile" type="file" accept=".bib" style="display: none">
			<button class="button is-primary">
				<label for="upload-button" style="cursor: pointer">
					<span class="icon-text">
						<span class="icon">
							<i class="mdi mdi-24px mdi-upload" />
						</span>
						<span>Upload</span>
					</span>
				</label>
			</button>
		</div>
	</section>
</template>

<style scoped>
.content-cell {
	padding-right: 4rem;
	vertical-align: middle;
	font-size: large;
}
</style>
