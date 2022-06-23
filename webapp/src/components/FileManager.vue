<script setup lang="ts">
import axios from "axios";
import { computed, ComputedRef, ref, Ref } from "vue";
import LoginForm from "@/components/LoginForm.vue";

const API_HOST = "localhost";
const API_PORT = "5000";

const NETWORK_ERROR_MESSAGE = "Unable to reach server. Please check your connection.";

const isLoading: Ref<boolean> = ref(false);

const login: Ref<string> = ref("");
const password: Ref<string> = ref("");

const token: Ref<string | null> = ref(sessionStorage.getItem("token"));
const hasToken: ComputedRef<boolean> = computed(() => token.value !== null);

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

function getToken(): void {
	token.value = sessionStorage.getItem("token");
	getFiles();
}

async function getFiles(): Promise<void> {
	clearError();
	await axios.get(
		`http://${API_HOST}:${API_PORT}/api/bibtex`,
		{
			headers: { Authorization: `${token.value}` },
		},
	)
		.then((response) => {
			items.value = [];
			response.data.forEach((item: any) => items.value.push(item));
		})
		.catch((error) => {
			if (error.response.status === 403) {
				clearToken();
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
}

async function postFile(event : Event & any): Promise<void> {
	clearError();
	isLoading.value = true;
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
		})
		.finally(() => isLoading.value = false);
}

async function restoreFile(id: number): Promise<void> {
	clearError();
	await axios.post(
		`http://${API_HOST}:${API_PORT}/api/bibtex/${id}`,
		{},
		{
			headers: {
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
	clearError();
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

getToken();
</script>

<template>
	<section class="section">
		<div class="container is-max-desktop">
			<LoginForm @loggedIn="getToken" v-if="!hasToken" />
			<div v-else>
				<h1 class="title has-text-centered">Bibtex files history</h1>
				<div v-if="hasError" class="notification is-danger">
					<p>
						{{ errorMessage }}
					</p>
				</div>

				<table v-if="items.length > 0" class="table is-striped is-fullwidth my-6">
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
								{{ new Date(item.uploaddate * 1000).toLocaleString("fr") }}
							</td>
							<td>
								<button @click="restoreFile(item.id)" class="button is-ghost">
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
					<input
						id="upload-button"
						@change="postFile"
						type="file"
						accept=".bib"
						:disabled="isLoading"
						style="display: none"
					>
					<label for="upload-button" class="button is-primary" :class="{ 'is-loading': isLoading }">
						<span class="icon-text">
							<span class="icon">
								<i class="mdi mdi-24px mdi-upload" />
							</span>
							<span>Upload</span>
						</span>
					</label>
					<p v-if="isLoading" class="mt-2">
						Converting bibtex file…
					</p>
				</div>
			</div>
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
