<script setup lang="ts">
import axios from "axios";
import { computed, ComputedRef, ref, Ref } from "vue";
import PasswordManager from "@/components/PasswordManager.vue";
import NewUserForm from "@/components/NewUserForm.vue";
import LoginForm from "@/components/LoginForm.vue";

const API_HOST = import.meta.env.API_HOST;
const API_PORT = import.meta.env.API_PORT;

const NETWORK_ERROR_MESSAGE = "Unable to reach server. Please check your connection.";

const login: Ref<string | null> = ref("");
const token: Ref<string | null> = ref("");
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
	getUsers();
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

getToken();
</script>

<template>
	<section class="section">
		<div class="container is-max-desktop">
			<LoginForm v-if="!hasToken" @logged-in="getToken" />
			<div v-else>
				<section class="section pt-0">
					<h1 class="title has-text-centered">
						{{ $t("Manage account") }}
					</h1>

					<p class="has-text-centered block">
						<span class="icon-text">
							<span class="icon">
								<i class="mdi mdi-check" />
							</span>
							<span>
								{{ $t("Connected as") }}
								<span class="has-text-primary">{{ login }}</span>.
							</span>
							<span class="icon" />
						</span>
					</p>

					<div class="block">
						<PasswordManager :token="token || ''" @invalid-token="clearToken" />
					</div>

					<div class="has-text-centered">
						<button class="button is-danger" @click="clearToken">
							<span class="icon-text">
								<span class="icon">
									<i class="mdi mdi-logout" />
								</span>
								<span>
									{{ $t("Log out") }}
								</span>
							</span>
						</button>
					</div>
				</section>
				<hr>
				<section class="section">
					<h1 class="title has-text-centered">
						{{ $t("Accounts list") }}
					</h1>
					<div v-if="hasError" class="notification is-danger">
						<p>
							{{ $t(errorMessage) }}
						</p>
					</div>

					<table class="table is-striped is-fullwidth my-6">
						<caption class="is-hidden">
							{{ $t("Application’s users") }}
						</caption>
						<thead>
							<tr>
								<th>
									{{ $t("Login") }}
								</th>
								<th>
									{{ $t("Admin") }}
								</th>
								<th />
							</tr>
						</thead>
						<tbody>
							<tr v-for="(user, i) in users" :key="i">
								<td class="content-cell">
									{{ user.login }}
								</td>
								<td class="content-cell">
									{{ $t(user.superadmin ? "Yes" : "No") }}
								</td>
								<td>
									<button
										class="button is-ghost has-text-danger"
										:class="{ 'is-invisible': user.superadmin }"
										@click="deleteUser(user.id)"
									>
										<span class="icon">
											<i class="mdi mdi-24px mdi-delete" />
										</span>
									</button>
								</td>
							</tr>
						</tbody>
					</table>

					<NewUserForm :token="token || ''" @invalid-token="clearToken" @new-user="getUsers" />
				</section>
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
