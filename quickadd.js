const { execSync } = require("child_process");

module.exports = async (params) => {
    const query = await params.quickAddApi.inputPrompt("Search notes:");
    if (!query) return;

    try {
        const result = execSync(
            `/home/alex/sync/obsidian/alex/ai_obsidian/run_search.sh "${query.replace(/"/g, '\\"')}"`,
            {
                encoding: "utf-8",
                maxBuffer: 10 * 1024 * 1024
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
        new Notice("Search failed — check console");
        console.log(e);
    }
};