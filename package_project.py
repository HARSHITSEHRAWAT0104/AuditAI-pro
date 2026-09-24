"""
AuditAI Pro - Cloud Deployment Packager
Creates a clean, production-ready ZIP archive of the project (excluding .venv and caches)
ready to upload directly to GitHub, Render, or Railway.
"""

import os
import zipfile

def package_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_filename = os.path.join(base_dir, "auditai_pro_deploy.zip")
    
    ignore_dirs = {".venv", "venv", "__pycache__", ".git"}
    ignore_files = {"auditai_pro_deploy.zip", ".env"}

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if file in ignore_files or file.endswith((".pyc", ".log")):
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname)

    print(f"[SUCCESS] Packaged clean deployment archive at: {zip_filename}")
    print(f"Size: {os.path.getsize(zip_filename) / 1024:.1f} KB")

if __name__ == "__main__":
    package_app()
