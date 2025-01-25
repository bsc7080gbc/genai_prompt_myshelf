
# MyShelf Data Template Documentation

This document explains the structure and fields in the MyShelf data JSON.

---

## **Structure Overview**

The JSON file is divided into two main sections:

- **MyBoxes**: Contains categorized data for reminders, notes, projects, shopping lists, and BlueSky (miscellaneous ideas or notes).
- **Metadata**: Contains metadata about the JSON, including versioning, timestamps, and a description.

---

### **1. MyBoxes**

#### **1.1. Reminders**
This section stores date-bound reminders.

```json
"Reminders": {
    "Date Bound": {
        "YYYY-MM-DDTHH:MM:SSZ": "Reminder Text"
    }
}
```

- **Fields**:
  - `YYYY-MM-DDTHH:MM:SSZ`: A date-time string in ISO 8601 format.
  - `"Reminder Text"`: The text of the reminder.

#### **1.2. Generic**
This section stores generic notes.

```json
"Generic": {
    "Note Title": "Note Text"
}
```

- **Fields**:
  - `"Note Title"`: A unique title for the note.
  - `"Note Text"`: The text of the note.

#### **1.3. Shopping**
This section stores categorized shopping lists.

```json
"Shopping": {
    "ListName": {
        "Items": ["Item 1", "Item 2"]
    }
}
```

- **Fields**:
  - `ListName`: A unique name for the shopping list.
  - `Items`: A list of items in the shopping list.

#### **1.4. BlueSky**
This section stores miscellaneous ideas or notes.

```json
"BlueSky": {
    "CategoryName": {
        "Note": "Category-specific note or idea"
    }
}
```

- **Fields**:
  - `CategoryName`: A category name for the idea or note.
  - `Note`: The text of the note.

---

### **2. Metadata**

```json
"Metadata": {
    "Version": "1.0.0",
    "Last Updated": "YYYY-MM-DDTHH:MM:SSZ",
    "Description": "Description of the JSON template"
}
```

- **Fields**:
  - `Version`: The version of the JSON schema.
  - `Last Updated`: A timestamp in ISO 8601 format indicating when the file was last updated.
  - `Description`: A description of the template and its purpose.

---

### **Usage Notes**

1. **Date Format**:
   All date fields must use the ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`).

2. **Naming Conventions**:
   - Use unique names for keys.
   
3. **Optional vs Required Fields**:
   - Fields like `Notes` (in Projects) and `Items` (in Shopping) can be left empty but should still follow the proper structure.
