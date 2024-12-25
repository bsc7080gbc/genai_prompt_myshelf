# MyShelf: Organize My Life

## Overview
MyShelf is a dynamic GenAI utility designed to enhance personal organization. It allows users to track reminders, store memories, manage ad-hoc information, and create categorized shopping lists. Simplification of what is required was the goal: ChatGPT + GitHub. Instructions have been provided to walk you through and explain the purpose and setup. I have also provided some historical versions as well so you can see how I matured the solution to where it is today.

In short, think "Jarvis" ...but on a budget.

---
**Read the Docs**:
   - [![User Manual](https://img.shields.io/badge/user%20manual-8A2BE2)](https://github.com/bsc7080gbc/genai_prompt_myshelf/wiki)
     - This manual provides instructions, feature overviews, and breakdowns of how this all works to help you get the most out of "MyShelf".
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
