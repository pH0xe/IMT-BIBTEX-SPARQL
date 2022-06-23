<script setup lang="ts">
import axios from "axios";
import { computed, ComputedRef, ref, Ref } from "vue";
import PasswordManager from "@/components/PasswordManager.vue";
import NewUserForm from "@/components/NewUserForm.vue";
import LoginForm from "@/components/LoginForm.vue";

const API_HOST = "localhost";
const API_PORT = "5000";

const NETWORK_ERROR_MESSAGE = "Unable to reach server. Please check your connection.";

const login: Ref<string | null> = ref(sessionStorage.getItem("login"));
const token: Ref<string | null> = ref(sessionStorage.getItem("token"));
const hasToken: ComputedRef<boolean> = computed(() => token.value !== null);

const errorMessage: Ref<string | undefined> = ref(undefined);
const hasError: ComputedRef<boolean> = computed(() => errorMessage.value !== undefined);

const users: Ref<any[]> = ref([]);

function clearError(): void {
	errorMessage.value = undefined;
}

function clearToken(): void {
	clearError();
	token.value = null;
	sessionStorage.removeItem("token");
}

function getToken(): void {
	token.value = sessionStorage.getItem("token");
	login.value = sessionStorage.getItem("login");
}

async function getUsers(): Promise<void> {
	clearError();
	await axios.get(
		`http://${API_HOST}:${API_PORT}/api/auth/users`,
		{
			headers: { Authorization: token.value || "" },
		},
	)
		.then((response) => {
			users.value = [];
			response.data.forEach((item: any) => users.value.push(item));
		})
		.catch((error) => {
			if (error.response.status === 401) {
				clearToken();
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
}

async function deleteUser(id: number): Promise<void> {
	clearError();
	await axios.delete(
		`http://${API_HOST}:${API_PORT}/api/auth/delete/${id}`,
		{
			headers: { Authorization: token.value || "" }
		},
	)
		.then(() => getUsers())
		.catch((error) => {
			if (error.response.status === 401) {
				clearToken();
			} else {
				errorMessage.value = NETWORK_ERROR_MESSAGE;
			}
		});
}

getUsers();
</script>

<template>
	<LoginForm @loggedIn="getToken" v-if="!hasToken" />
	<div v-else>
		<section class="section">
			<h1 class="title has-text-centered">Users</h1>
			<div v-if="hasError" class="notification is-danger">
				<p>
					{{ errorMessage }}
				</p>
			</div>

			<table class="table container is-striped my-6">
				<caption class="is-hidden">Application’s users</caption>
				<thead>
					<tr>
						<th>
							Login
						</th>
						<th>
							Admin
						</th>
						<th />
					</tr>
				</thead>
				<tbody>
					<tr v-for="(user, i) in users" key="i">
						<td class="content-cell">
							{{ user.login }}
						</td>
						<td class="content-cell">
							{{ user.superadmin }}
						</td>
						<td>
							<button v-if="!user.superadmin" @click="deleteUser(user.id)" class="button is-ghost has-text-danger">
								<span class="icon">
									<i class="mdi mdi-24px mdi-delete" />
								</span>
							</button>
						</td>
					</tr>
				</tbody>
			</table>

			<NewUserForm :token="token || ''" @invalidToken="clearToken" @newUser="getUsers" />
		</section>
		<section class="has-text-centered">
			<h1 class="title">Manage account</h1>

			<p>Connected as <span class="has-text-primary">{{ login }}</span>.</p>

			<PasswordManager :token="token || ''" @invalidToken="clearToken" />
		</section>
	</div>
</template>

<style scoped>
.content-cell {
	padding-right: 4rem;
	vertical-align: middle;
	font-size: large;
}
</style>
