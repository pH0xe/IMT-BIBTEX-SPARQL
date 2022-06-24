import { createI18n } from "vue-i18n";

const files = import.meta.globEager("@/locales/*.json");

export default createI18n({
	locale: navigator.language.split("-")[0] || "en",
	fallbackLocale: "en",
	messages: Object.fromEntries(
		Object.keys(files).map((path: string): Record<string, string>[] => (
			[(path.match(/[a-z]+(?=.json)/) || [""])[0], files[path].default]
		)),
	),
});
