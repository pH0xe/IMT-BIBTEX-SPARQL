<script setup lang="ts">
import axios from "axios";
import { ref, Ref } from "vue";

const items: Ref<any[]> = ref([]);

async function getFiles(): Promise<void> {
	items.value = [];
	await axios.get('http://localhost:8081/api/bibtex')
		.then((response) => response.data.forEach((item: any) => items.value.push(item)))
		.catch((error) => console.error(error));
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
	});
	getFiles();
}

async function deleteFile(id: number): Promise<void> {
	await axios.delete(`http://localhost:8081/api/bibtex/${id}`);
	getFiles();
}

getFiles();
</script>

<template>
	<table>
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
				<td>
					{{ item.name }}
				</td>
				<td>
					{{ new Date(item.uploadDate).toLocaleString("fr") }}
				</td>
				<td>
					<button @click="deleteFile(item.id)">Delete</button>
				</td>
			</tr>
		</tbody>
	</table>
	<input id="upload-button" @change="postFile" type="file" accept=".bib" style="display: none">
	<button style="width: max-content">
		<label for="upload-button" style="cursor: pointer">Upload</label>
	</button>
</template>

<style scoped>
</style>
