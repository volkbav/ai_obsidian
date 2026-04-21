const { execSync } = require("child_process");

module.exports = async (params) => {
    const query = await params.quickAddApi.inputPrompt("Search notes:");
    if (!query) return;

    try {
        const vaultPath = app.vault.adapter.basePath;

        const uvPath = "/snap/bin/uv"; // ← ВАЖНО

        const result = execSync(
            `${uvPath} run python search.py "${query.replace(/"/g, '\\"')}"`,
            {
                encoding: "utf-8",
                cwd: `${vaultPath}/ai_obsidian`,
                stdio: "pipe"
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

    } catch (error) {
        new Notice("Search failed — see console");

        console.log("STDOUT:", error.stdout?.toString());
        console.log("STDERR:", error.stderr?.toString());
        console.log(error);
    }
};