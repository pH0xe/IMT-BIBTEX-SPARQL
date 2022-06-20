<script setup lang="ts">
import axios from "axios";
import { ref, Ref } from "vue";

const items: Ref<any[]> = ref([]);

const hasError: Ref<boolean> = ref(false);

async function getFiles(): Promise<void> {
	items.value = [];
	await axios.get('http://localhost:8081/api/bibtex')
		.then((response) => response.data.forEach((item: any) => items.value.unshift(item)))
		.catch(() => hasError.value = true);
}

async function postFile(event : Event & any): Promise<void> {
	await axios.post(
		'http://localhost:8081/api/bibtex',
		{
			file: event.target!.files[0],
		}, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	})
		.then(() => getFiles())
		.catch(() => hasError.value = true);
}

async function deleteFile(id: number): Promise<void> {
	await axios.delete(`http://localhost:8081/api/bibtex/${id}`)
		.then(() => getFiles())
		.catch(() => hasError.value = true);
}

getFiles();
</script>

<template>
	<section class="section">
		<h1 class="title has-text-centered">Bibtex files history</h1>
		<div v-if="hasError" class="notification is-danger">
			<p>
				Unable to reach server. Please check your connection.
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
