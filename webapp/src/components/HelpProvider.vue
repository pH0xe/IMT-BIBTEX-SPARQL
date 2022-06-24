<script setup lang="ts">
</script>

<template>
	<section class="section">
		<div class="container is-max-desktop">
			<h1 class="title has-text-centered">
				{{ $t("Help") }}
			</h1>
			<article class="content">
				<h3>{{ $t("Upload file") }}</h3>
				<p>
					{{ $t("Firstly, upload a valid bibtex file in") }}
					<router-link to="files">
						{{ $t("Files") }}
					</router-link>
					.
					{{ $t("Use the button “Upload File”.") }}
					{{ $t("The process can take several minutes for long files.") }}
					{{ $t("Then, the data are updated and the file is added to the history.") }}
					{{ $t("You can restore older files, but the conversion process will be restarted from the beginning.") }}
					{{ $t("Each file loading erases the previous data.") }}
					{{ $t("Finally, online files deletion is possible but definitive.") }}
				</p>
				<h3>{{ $t("Do research") }}</h3>
				<p>
					{{ $t("Once data are loaded, you can use") }}
					<router-link to="sparklis">
						Sparklis
					</router-link>
					{{ $t("to do research in natural language.") }}
					{{ $t("It uses the") }}
					<a href="https://www.w3.org/RDF/" target="_blank">
						RDF
					</a>
					{{ $t("technology to work.") }}
					<a href="https://www.youtube.com/watch?v=O999FVXn8Qc" target="_blank">
						{{ $t("This video") }}
					</a>
					{{ $t("explains how to use the tool.") }}
				</p>
				<h3>{{ $t("Change password") }}</h3>
				<p>
					{{ $t("You need to be logged in to manage files and other accounts.") }}
					{{ $t("To edit your password, go to") }}
					<router-link to="account">
						{{ $t("Accounts") }}
					</router-link>
					{{ $t("and edit your password there.") }}
				</p>
				<h3>{{ $t("Account management") }}</h3>
				<p>
					{{ $t("Once logged in, you can create other accounts in") }}
					<router-link to="account">
						{{ $t("Accounts") }}
					</router-link>
					{{ $t("or even delete them.") }}
					{{ $t("Accounts must have all different logins.") }}
					{{ $t("It is impossible to delete the admin account.") }}
				</p>
			</article>
		</div>
	</section>
</template>
