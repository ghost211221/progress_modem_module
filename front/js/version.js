$(document).ready(async function() {
    version = await eel.get_version()();
    document.title = `Графическая программа настройки модуля ПН6280 ИЛТА.464512.005 v${version}`
})