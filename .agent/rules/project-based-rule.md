---
trigger: always_on
---

# Project basic rule

## Basic Information
This is an **HTML injection scripting project**. Its core objective is to **customize the VS Code AI chat window iframe interface** (e.g., modifying AI response colors, adding copy buttons).
The project uses a **direct HTML replacement** model: users simply replace the original file with the modified HTML file for changes to take effect.

## Rules
- **Single File Principle**: All custom JS, CSS, and added HTML logic must be written inline directly within the `workbench.html` file.
- **Zero Dependencies**: Do not rely on any external libraries or build tools; use pure, native HTML/CSS/JS.
- **KISS Principle**: Keep the implementation as simple as possible to make copying and replacing the file easy for users.
- **Beginner Friendly**: Code and comments should be clear so users can easily understand and modify the code themselves.

## Architecture
1. **CSS Layer**: Use inline `<style>` tags to define all style overrides and custom themes.
2. **JS Layer**: Use inline `<script>` tags to implement DOM observation, style injection, and feature enhancements (like copy buttons).
3. **HTML Layer**: Append necessary containers or elements alongside the existing DOM structure.

## Development Environment
- **OS**: Mac OS (Host)
- **Project Root**: `/Volumes/eeBox/eeProject/lm802.4.14.6.25`
- **App Director**: `./app_root`
- **Core File**: `./app_root/workbench.html`

## Design Requirements
- Themes should be clean, refined, professional, aesthetically pleasing, and grand.
- Features should be highly configurable, with JS variables controlling feature toggles (like colors and buttons).

## Workflow Auto-matching
- This project involves two types of workflows. Automatically map tasks to the workflows below:
    - Core HTML page modifications/design work maps to `html-worker` (.agent/workflows/html-worker.md)
    - `workbench.html` feature development maps to `anti-better-worker` (.agent/workflows/anti-better-worker.md)
    - Otherwise use the default workflow.

## Core Project File
- `app_root/workbench.html`: The HTML file for the AI sidebar. All custom code for V0.2 is written here.

## How to Use
Users simply copy and replace their IDE's equivalent file with the modified `workbench.html`.