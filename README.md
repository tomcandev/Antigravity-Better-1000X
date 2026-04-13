<div align="center">
  <h1>🚀 Antigravity-Better-1000X</h1>
  <p><strong>Customize your Antigravity AI chat panel. Your IDE, your rules.</strong></p>
  <br>
  <p>
    <img src="https://img.shields.io/badge/version-0.2.10-brightgreen" alt="Version">
    <img src="https://img.shields.io/badge/dependencies-zero-green" alt="Zero Dependencies">
    <img src="https://img.shields.io/badge/file-single%20HTML-blue" alt="Single File">
  </p>
  <p>
    <i>Inspired by the original <a href="https://github.com/016/Antigravity-Better">016/Antigravity-Better</a> project.</i> 
    <br>
    <i>Refactored and maintained for English-first workflows.</i>
  </p>
</div>

---

## ✨ What is Antigravity-Better-1000X?

**Antigravity-Better-1000X** is a lightweight toolkit for customizing the AI chat panel in Google's AI-powered IDE.

By simply dropping **one HTML file** into your IDE's core structure, you can unlock powerful chat panel customizations—without touching source code or installing complex extensions.

### Key Features
- **Custom Fonts & Colors**: Dynamically set specific colors and font sizes for AI responses vs User queries.
- **Auto-Accept Diff Operations**: Configurable automatic accept for diff operations to speed up repetitive code generation.
- **Keyboard Shortcuts**: Map your own shortcuts (e.g., `Cmd + Enter`) for sending messages to the AI.
- **LaTeX Math Support**: Automatic rendering of mathematical formulas in AI outputs.
- **One-Click Copy**: Injected quick copy buttons for code blocks and outputs.
- **Zero Overhead**: Fully vanilla JavaScript with disabled features costing exactly zero performance.

---

## 📦 Installation

### Quick Start (macOS Example)

1. **Locate the target file path in your IDE installation:**
   ```
   /Applications/Antigravity.app/Contents/Resources/app/out/vs/code/electron-browser/workbench/workbench.html
   ```

2. **Backup & Replace file via Terminal**
   ```bash
   cd /Applications/Antigravity.app/Contents/Resources/app/out/vs/code/electron-browser/workbench/

   # Backup original
   cp workbench.html workbench.html.bak
   
   # Replace with Antigravity-Better-1000X
   cp /path/to/Antigravity-Better-1000X/app_root/workbench.html ./
   ```

3. **Restart your IDE** - Done! 🎉

> ⚠️ **Note**: Every time the IDE updates, it will overwrite the HTML file. You'll need to re-apply this replacement after each update. Alternatively, use the included Python deployment tool `deploy_tool.py` to automate the replacement mapping.

---

## 🛠️ Usage & Customization

Click the **⚙️ floating button** on the right side of your IDE chat panel to open the embedded Settings Menu. From there, you can toggle features on and off dynamically. 

### Adding Your Own Features
You can freely customize the core `workbench.html` file to build your own tools. Antigravity-Better-1000X is designed with performance isolation in mind:

```html
<style>
  /* 1. Add your CSS - only active when feature class is present */
  #react-app.your-feature .target { color: red; }
</style>

<script>
  // 2. Add your config
  const YOUR_CONFIGS = [{ id: 'my-feature', ... }];
  
  // 3. Implement your logic
  function applyYourFeature() {
    if (!currentSettings.yourFeatureEnabled) return;
    // Your execution logic here...
  }
</script>
```

---

## 📜 Credits & License

- Original architectural concepts and inspiration by [016/Antigravity-Better](https://github.com/016/Antigravity-Better).
- MIT License. Feel free to use, modify, and share.
