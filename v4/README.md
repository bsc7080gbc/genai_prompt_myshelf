# MyShelf: Organize My Life

## Overview
MyShelf is a dynamic GenAI utility designed to enhance personal organization. It allows users to track reminders, store memories, manage ad-hoc information, and create categorized shopping lists. Simplification of what is required was the goal: ChatGPT + GitHub. Instructions have been provided to walk you through and explain the purpose and setup. I have also provided some historical versions as well so you can see how I matured the solution to where it is today.

In short, think "Jarvis" ...but on a budget.

---

# Ziggy: Data Automation System

Ziggy simplifies data management and automation using GitHub workflows. It handles tasks like syncing, archiving, and cleanup while maintaining flexibility for custom workflows. Powered by your Custom GPT setup, it ensures reliability without databases or middleware.

## Features
- **Voice-Activated Interaction**: Engage with MyShelf using voice commands - courtesty of ChatGPT.
- **Dynamic Categorization**: Manage various categories such as goals, inventory, and to-dos. Each category is stored in boxes, with the ability to nest boxes for detailed organization.
- **Reminders**: Set reminders with specific countdowns (e.g., 30 days, 15 days, 1 day, etc.) and receive alerts as deadlines approach.
- **Editable Content**: Add, remove, or inquire about the contents of any box at any time.
- **Version Control**: Track changes and manage versions through integration with GitHub or a similar platform.
- **Workflows**: Automate tasks like syncing (`syncdata.yml`), archiving (`archivedata.yml`), and cleanup (`purgedata.yml`).
- **Custom Automation**: Tailor workflows for personal or professional use.

## How It Works
1. **Create and Label Boxes**: Start by creating boxes, which serve as categories or classifications for storing related items.
2. **Nested Boxes**: Further organize by creating nested boxes within primary boxes.
3. **Add Items**: Populate boxes with items or tasks as needed.
4. **Set Reminders**: Use the reminders feature to set specific timelines for tasks or remember important dates.
5. **Interact and Query**: At any point, interact with MyShelf to add, remove, or query items within the boxes.

## Storage Solution
Improved long-term memory barrier by using GitHub repository, ensuring read/write access and data persistence.

## Getting Started
1. **Read the Docs**:
   - Read [Project_MyShelf.md](https://github.com/bsc7080gbc/genai_prompt_myshelf/blob/main/v4/Project_%20MyShelf.md)
2. **Once setups are completed**:
   - Stage `data.json` in your private repo
   - From within your private Custom GPT, retrieve and update `data.json` as needed:
     ```
     retrieve data.json from remote root path=data.json
     ```
     ```
     add "quantum computer" to groceries list. publish to remote. path=updates/data.json
     ```
   - Add reminders, add new 'boxes' for organization. Experiment. 

## Links
- [Repository](https://github.com/bsc7080gbc/genai_prompt_myshelf)
- [Project Board](https://github.com/users/bsc7080gbc/projects/1)
- [Short Video Demo (older but still a good walk through)](https://drive.google.com/file/d/10l9scfqsa1pOdL_T76dOz_NmJxbZpfbo/view?usp=drive_link)
- [Action Plan Demo](https://drive.google.com/file/d/14wF28FchBIZ2Zv0MxqtR8SeMTxDVN9xO/view?usp=drivesdk)
- [Prior Versions](https://github.com/bsc7080gbc/genai_prompt_myshelf/tree/main/archive)

## Feedback
Your feedback is invaluable to me. Please submit any feedback, issues, or feature requests through the GitHub issues page or contact us directly.







