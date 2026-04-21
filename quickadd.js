const { execSync } = require("child_process");

module.exports = async (params) => {
    const query = await params.quickAddApi.inputPrompt("Search notes:");
    if (!query) return;

    try {
        const vaultPath = app.vault.adapter.basePath;

        // 🔥 ВАЖНО: абсолютный путь к uv
        const uvPath = "/snap/bin/uv";

        const command = `${uvPath} run python search.py "${query.replace(/"/g, '\\"')}"`;

        const result = execSync(command, {
            encoding: "utf-8",
            cwd: `${vaultPath}/ai_obsidian`,
            maxBuffer: 1024 * 1024 * 10,
            env: {
                ...process.env,
                PYTHONIOENCODING: "utf-8"
            }
        });

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

        console.log("========== DEBUG ==========");
        console.log(error.stdout?.toString() || "no stdout");
        console.log(error.stderr?.toString() || "no stderr");
        console.log(error);
        console.log("===========================");

        return;
    }
};