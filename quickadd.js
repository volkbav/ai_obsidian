const { execSync } = require("child_process");

module.exports = async (params) => {
    const query = await params.quickAddApi.inputPrompt("Search notes:");
    if (!query) return;

    try {
        const vaultPath = app.vault.adapter.basePath;
        const safeQuery = query.replace(/"/g, '\\"');

        const result = execSync(
            `python search.py "${safeQuery}"`,
            {
                encoding: "utf-8",
                maxBuffer: 1024 * 1024 * 10,
                cwd: `${vaultPath}/ai_obsidian`
            }
        );

        const folder = "AI Search";

        if (!app.vault.getAbstractFileByPath(folder)) {
            await app.vault.createFolder(folder);
        }

        let fileName = `${folder}/AI Search - ${query}.md`;
        let counter = 1;

        while (app.vault.getAbstractFileByPath(fileName)) {
            fileName = `${folder}/AI Search - ${query} (${counter}).md`;
            counter++;
        }

        const file = await app.vault.create(
            fileName,
            `# ${query}\n\n${result}`
        );

        await app.workspace.getLeaf().openFile(file);

    } catch (e) {
        new Notice("Search failed");
        console.error(e);
    }
};