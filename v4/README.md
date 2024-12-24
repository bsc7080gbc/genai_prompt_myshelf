# Ziggy: Data Automation System

Ziggy simplifies data management and automation using GitHub workflows. It handles tasks like syncing, archiving, and cleanup while maintaining flexibility for custom workflows. Powered by a private GPT setup, it ensures reliability without databases or middleware.

## Features
- **Dynamic Data**: Easily update and manage JSON files.
- **Workflows**: Automate tasks like syncing (`syncdata.yml`), archiving (`archivedata.yml`), and cleanup (`purgedata.yml`).
- **Custom Automation**: Tailor workflows for personal or professional use.

## Getting Started
1. **Read the Docs**:
   - Read `Project_MyShelf.docx` or `Project_MyShelf.pdf`.
2. **Once setups are completed**:
   - Stage `data.json` in your private repo
   - From within your private Custom GPT, retrieve and update `data.json` as needed:
     ```
     retrieve data.json from remote root path=data.json
     add "quantum computer" to groceries list. publish to remote. path=updates/data.json
     ```

## Links
- [Repository](https://github.com/bsc7080gbc/genai_prompt_myshelf)
- [Project Board](https://github.com/users/bsc7080gbc/projects/1)

