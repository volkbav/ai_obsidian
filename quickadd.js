const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

module.exports = async (params) => {
    const query = await params.quickAddApi.inputPrompt("Search notes:");
    if (!query) return;

    try {
        // читаем .env
        const envPath = "/home/alex/it/ai_obsidian/.env";  //надо указать путь до проекта
        const env = fs.readFileSync(envPath, "utf-8");

        const getEnv = (key) => {
            const match = env.match(new RegExp(`${key}=(.*)`));
            return match ? match[1].trim() : null;
        };

        const projectPath = getEnv("PROJECT_PATH");
        const pythonPath = getEnv("PYTHON_PATH");

        const result = execSync(
            `${pythonPath} search.py "${query}"`,
            {
                encoding: "utf-8",
                maxBuffer: 1024 * 1024 * 10,
                cwd: projectPath
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
            `# ${fileName}\n\n${result}`
        );

        await app.workspace.getLeaf().openFile(file);

    } catch (error) {
        new Notice("Search failed");
        console.error(error);
    }
};