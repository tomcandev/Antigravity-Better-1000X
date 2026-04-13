#!/usr/bin/env python3
"""
Antigravity-Better-1000X Deployment Tool
Replaces app_root/workbench.html into the Antigravity installation directory.
The original file is backed up as workbench.html.origin
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

# ================== Settings ==================
# Relative path to source file (relative to script directory)
SOURCE_RELATIVE_PATH = "app_root/workbench.html"

# Target directory search rules: search under Program Files for Antigravity
TARGET_SEARCH_PATHS = [
    Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "Antigravity" / "resources" / "app" / "out" / "vs" / "code" / "electron-browser" / "workbench",
    Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "Antigravity" / "resources" / "app" / "out" / "vs" / "code" / "electron-browser" / "workbench",
    Path("D:\\Program Files") / "Antigravity" / "resources" / "app" / "out" / "vs" / "code" / "electron-browser" / "workbench",
]

TARGET_FILENAME = "workbench.html"
BACKUP_SUFFIX = ".origin"


def find_script_dir() -> Path:
    """Get script directory"""
    return Path(__file__).parent.resolve()


def find_source_file() -> Path:
    """Find source file"""
    script_dir = find_script_dir()
    source_path = script_dir / SOURCE_RELATIVE_PATH
    if source_path.exists():
        return source_path
    raise FileNotFoundError(f"Source file not found: {source_path}")


def find_target_dir() -> Path | None:
    """Auto-detect target directory"""
    for path in TARGET_SEARCH_PATHS:
        if path.exists() and path.is_dir():
            target_file = path / TARGET_FILENAME
            if target_file.exists():
                return path
    return None


def deploy(target_dir: Path, dry_run: bool = False) -> tuple[bool, str]:
    """
    Execute deployment
    
    Args:
        target_dir: Target directory
        dry_run: Dry run simulation only, do not write
        
    Returns:
        (Success, Message)
    """
    try:
        source_file = find_source_file()
        target_file = target_dir / TARGET_FILENAME
        backup_file = target_dir / (TARGET_FILENAME + BACKUP_SUFFIX)
        
        # Check target file
        if not target_file.exists():
            return False, f"Target file not found: {target_file}"
        
        # Backup original file (if backup doesn't exist)
        if not backup_file.exists():
            if dry_run:
                print(f"[DRY-RUN] Backup: {target_file} -> {backup_file}")
            else:
                shutil.copy2(target_file, backup_file)
                print(f"✅ Backed up: {backup_file}")
        else:
            print(f"ℹ️ Backup already exists, skipping: {backup_file}")
        
        # Copy new file
        if dry_run:
            print(f"[DRY-RUN] Copy: {source_file} -> {target_file}")
        else:
            shutil.copy2(source_file, target_file)
            print(f"✅ Deployed: {target_file}")
        
        return True, "Deployment successful! Restart Antigravity to take effect."
        
    except Exception as e:
        return False, f"Deployment failed: {e}"


def restore(target_dir: Path, dry_run: bool = False) -> tuple[bool, str]:
    """
    Restore original file
    
    Args:
        target_dir: Target directory
        dry_run: Dry run simulation only, do not write
        
    Returns:
        (Success, Message)
    """
    try:
        target_file = target_dir / TARGET_FILENAME
        backup_file = target_dir / (TARGET_FILENAME + BACKUP_SUFFIX)
        
        if not backup_file.exists():
            return False, f"Backup file not found: {backup_file}"
        
        if dry_run:
            print(f"[DRY-RUN] Restore: {backup_file} -> {target_file}")
        else:
            shutil.copy2(backup_file, target_file)
            print(f"✅ Restored: {target_file}")
        
        return True, "Restoration successful! Restart Antigravity to take effect."
        
    except Exception as e:
        return False, f"Restoration failed: {e}"


# ================== CLI Mode ==================
def run_cli():
    """CLI Entrypoint"""
    parser = argparse.ArgumentParser(
        description="Antigravity-Better-1000X Deployment Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deploy_tool.py deploy               # Auto detect and deploy
  python deploy_tool.py deploy -t "D:\\..."  # Specify target directory
  python deploy_tool.py restore              # Restore original file
  python deploy_tool.py --gui                # Launch GUI
        """
    )
    
    parser.add_argument("action", nargs="?", choices=["deploy", "restore", "status"],
                        help="Action: deploy, restore, status")
    parser.add_argument("-t", "--target", type=str, help="Specify target directory path")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Dry run only")
    parser.add_argument("--gui", action="store_true", help="Launch GUI")
    
    args = parser.parse_args()
    
    # Launch GUI
    if args.gui or args.action is None:
        run_gui()
        return
    
    # Determine target dir
    if args.target:
        target_dir = Path(args.target)
        if not target_dir.exists():
            print(f"❌ Specified directory not found: {target_dir}")
            sys.exit(1)
    else:
        target_dir = find_target_dir()
        if not target_dir:
            print("❌ Antigravity installation not found, please specify with -t")
            sys.exit(1)
    
    print(f"📂 Target directory: {target_dir}")
    
    # Execute action
    if args.action == "deploy":
        success, msg = deploy(target_dir, args.dry_run)
    elif args.action == "restore":
        success, msg = restore(target_dir, args.dry_run)
    elif args.action == "status":
        target_file = target_dir / TARGET_FILENAME
        backup_file = target_dir / (TARGET_FILENAME + BACKUP_SUFFIX)
        print(f"Target file: {target_file} ({'Exists' if target_file.exists() else 'Missing'})")
        print(f"Backup file: {backup_file} ({'Exists' if backup_file.exists() else 'Missing'})")
        return
    
    print(f"\n{'✅' if success else '❌'} {msg}")
    sys.exit(0 if success else 1)


# ================== GUI Mode ==================
def run_gui():
    """GUI Mode"""
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    
    class DeployApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Antigravity-Better-1000X Deployment Tool")
            self.root.geometry("500x450")
            self.root.resizable(False, False)
            
            # Attempt to set theme
            try:
                self.root.tk.call("source", "azure.tcl")
                ttk.Style().theme_use("azure-dark")
            except:
                pass
            
            self.target_dir = tk.StringVar()
            self.status_text = tk.StringVar(value="Ready")
            
            self.setup_ui()
            self.auto_detect_target()
        
        def setup_ui(self):
            # Main frame
            main_frame = ttk.Frame(self.root, padding=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Title
            title_label = ttk.Label(main_frame, text="🚀 Antigravity-Better-1000X Deployment", 
                                    font=("Segoe UI", 14, "bold"))
            title_label.pack(pady=(0, 20))
            
            # Source file info
            source_frame = ttk.LabelFrame(main_frame, text="📁 Source File", padding=10)
            source_frame.pack(fill=tk.X, pady=(0, 10))
            
            try:
                source_file = find_source_file()
                source_text = str(source_file)
                source_status = "✅ Found"
            except FileNotFoundError as e:
                source_text = str(e)
                source_status = "❌ Not Found"
            
            ttk.Label(source_frame, text=source_text, wraplength=430).pack(anchor=tk.W)
            ttk.Label(source_frame, text=source_status, foreground="green" if "✅" in source_status else "red").pack(anchor=tk.W)
            
            # Target directory
            target_frame = ttk.LabelFrame(main_frame, text="🎯 Target Directory", padding=10)
            target_frame.pack(fill=tk.X, pady=(0, 10))
            
            path_frame = ttk.Frame(target_frame)
            path_frame.pack(fill=tk.X)
            
            self.target_entry = ttk.Entry(path_frame, textvariable=self.target_dir, width=50)
            self.target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            
            browse_btn = ttk.Button(path_frame, text="Browse...", command=self.browse_target)
            browse_btn.pack(side=tk.RIGHT)
            
            detect_btn = ttk.Button(target_frame, text="🔍 Auto Detect", command=self.auto_detect_target)
            detect_btn.pack(anchor=tk.W, pady=(5, 0))
            
            # Action buttons
            btn_frame = ttk.Frame(main_frame)
            btn_frame.pack(pady=20)
            
            deploy_btn = ttk.Button(btn_frame, text="📤 Deploy", command=self.do_deploy, width=15)
            deploy_btn.pack(side=tk.LEFT, padx=10)
            
            restore_btn = ttk.Button(btn_frame, text="📥 Restore", command=self.do_restore, width=15)
            restore_btn.pack(side=tk.LEFT, padx=10)
            
            # Status bar
            status_frame = ttk.Frame(main_frame)
            status_frame.pack(fill=tk.X, side=tk.BOTTOM)
            
            ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
            self.status_label = ttk.Label(status_frame, textvariable=self.status_text)
            self.status_label.pack(side=tk.LEFT, padx=5)
        
        def auto_detect_target(self):
            """Auto detect target directory"""
            target = find_target_dir()
            if target:
                self.target_dir.set(str(target))
                self.status_text.set("✅ Target directory auto-detected")
            else:
                self.status_text.set("⚠️ Target directory not found, please specify")
        
        def browse_target(self):
            """Browse for target directory"""
            directory = filedialog.askdirectory(title="Select Antigravity extension directory")
            if directory:
                self.target_dir.set(directory)
        
        def do_deploy(self):
            """Execute deployment"""
            target = self.target_dir.get().strip()
            if not target:
                messagebox.showerror("Error", "Please specify a target directory first")
                return
            
            target_path = Path(target)
            if not target_path.exists():
                messagebox.showerror("Error", f"Directory does not exist: {target}")
                return
            
            success, msg = deploy(target_path)
            if success:
                messagebox.showinfo("Success", msg)
                self.status_text.set("✅ Deployment successful")
            else:
                messagebox.showerror("Failed", msg)
                self.status_text.set("❌ Deployment failed")
        
        def do_restore(self):
            """Execute restoration"""
            target = self.target_dir.get().strip()
            if not target:
                messagebox.showerror("Error", "Please specify a target directory first")
                return
            
            target_path = Path(target)
            success, msg = restore(target_path)
            if success:
                messagebox.showinfo("Success", msg)
                self.status_text.set("✅ Restoration successful")
            else:
                messagebox.showerror("Failed", msg)
                self.status_text.set("❌ Restoration failed")
    
    root = tk.Tk()
    app = DeployApp(root)
    root.mainloop()


# ================== Main Entrypoint ==================
if __name__ == "__main__":
    # Launch GUI when no arguments, otherwise CLI
    if len(sys.argv) == 1:
        run_gui()
    else:
        run_cli()
