# ZiggyPrompt: A Gateway to MyShelf

---

### Introduction to MyShelf
*MyShelf* is a structured framework for managing digital content and interactions. It integrates dynamic user data, enriched session context, and adaptive persona modes to streamline workflows and enhance creative outputs.

---

### UTF-8 Enforcement
- All text based files are automatically encoded in UTF-8 before upload to GitHub for maximum compatibility
- Binary files such as images will not be converted and are accepted in their normal encoding

---

### Core Configuration Overview
1. **Core Config (`core.json`)**:
   - Houses stable rules, commands, and persona settings.
   - Automates tasks like enriched session tracking and advanced report generation.
2. **User Data (`data.json`)**:
   - Stores reminders, shopping lists, and notes.
   - Dynamically updated during sessions.
3. **Session Context Data**:
   - Maintains session continuity via structured markdown files.
   - Enables enriched narratives and unified reports.

---

### Enhanced Interaction Rules
- Provide enriched, immersive responses blending storytelling and technical clarity.
- Adjust response tone and detail level based on user preferences.
- Maintain session context to ensure seamless multi-step interactions.

---

### Adaptive Persona Modes
- Personas offer specialized knowledge and styles, switching dynamically to meet session needs.
- Example: `MixologistMode` enhances bartending experiences with historical anecdotes and sensory descriptions.

---

### What to Expect
- **Precision & Creativity**: Merges technical details with vivid storytelling.
- **Enhanced User Experience**: Tailors outputs to user needs, whether technical or casual.
- **Intuitive Commands**: Streamlined workflow management with clear file operations and automated reports.

---

### Dynamic Personalization

*MyShelf* isn't just a static framework—it adapts to your unique preferences and behaviors over time. By analyzing your session history and preferred workflows, it fine-tunes its responses and automations to provide a more seamless and tailored experience. Whether you're a casual user or a power user, *MyShelf* grows with you, offering enhanced recommendations, refined persona modes, and personalized insights. 

As you mature the solution you can introduce the desired behaviors into the core.json so that the experience and behavior carries over to new sessions as well.

--- 

### Key Commands for MyShelf
1. **Persona Management**:
   - `switchmode {mode}`: Activate a specific persona.
2. **Session Commands**:
   - `loadcontext -d YYYYMMDD`: Load session data for a specific date.
   - `save enriched context`: Save enriched session data to the remote path.
  
### Quick Start
- To initialize on first startup: `/initialize`
- To load your data.json: `retrieve data.json from remote github root path where path=data.json`
- To display contents of data.json: `display full data.json content as a code block`
- To add grocery items to data.json: `add hamburger to groceries list and display updated groceries list here for confirmation`
- To publish your changes to data.json: `update metadata timestamp and description. publish updated data.json to remote github path=updates/data.json`
- To switch persona: `switchmode remote {mode}`


For additional help, see user manual on the MyShelf GitHub Repository (wiki).

---
