# AI Obsidian - Поиск по заметкам Obsidian с помощью AI

Поиск по заметкам Obsidian с использованием векторной базы данных ChromaDB и локальной модели эмбеддингов Ollama.

## Установка

1. Скопируйте проект внутрь вашего Obsidian vault:
```
ObsidianVault/
├── AI Search/              (результаты поиска)
├── wiki/                   (ваши заметки)
├── daily/
├── ai_obsidian/           ← ПРОЕКТ ЗДЕСЬ
│   ├── index.py
│   ├── search.py
│   ├── .env
│   └── chroma_db/
```

2. Установите зависимости:
```bash
uv sync
```

3. Создайте файл `.env` в корне проекта:
```env
VAULT_PATH=/путь/к/вашему/vault
OLLAMA_URL=http://localhost:11434/api/embeddings
MODEL=nomic-embed-text
CHROMA_PATH=./chroma_db
CHUNK_SIZE=500
CHUNK_OVERLAP=100
```

## Использование

### Проверка Ollama
- проверка наличия модели
```bash
curl http://localhost:11434/api/tags | grep nomic-embed-text
```
- если в ответе отсутствует нужная модель - необходимо её установить: [поиск моделей](https://ollama.com/search?c=embedding)

### Индексация заметок

Индексирует все `.md` файлы из вашего vault в ChromaDB:

```bash
uv run python3 index.py
```

### Поиск в терминале

Поиск по индексированным заметкам:

```bash
uv run python3 search.py "ваш запрос"
```

Пример:
```bash
uv run python search.py "как настроить Python в VS Code"
```

### Подключение к обсидиан
- Необходимо установить расширение `QuickAdd`.
- папку с проектом скопировать в корень папки с заметками
- добавить в настройках `QuickAdd`: `Choices&Packages` -> `Macro`: в настройках добавить `User Script` - `quickadd` (обсидиан его сам найдет, если проект расположен в хранилище)

## Архитектура

- **index.py** — индексирует заметки, разбивает на чанки, генерирует эмбеддинги и сохраняет в ChromaDB
- **search.py** — выполняет поиск по векторному индексу и возвращает релевантные фрагменты
- **debug.py** — отладочный скрипт для проверки состояния базы данных

## Зависимости

- `chromadb` — векторная база данных
- `python-dotenv` — загрузка переменных окружения
- `requests` — запросы к Ollama API
- `tqdm` — прогресс-бар при индексации

## Требования

- Python 3.12+
- Ollama с установленной моделью эмбеддингов (по умолчанию `nomic-embed-text`)
- Obsidian vault с заметками и плагином QuickAdd
