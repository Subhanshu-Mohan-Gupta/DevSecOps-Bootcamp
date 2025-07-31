import os
print("\n--- Auto Checker ---")
for folder in os.listdir("."):
    if folder.startswith("T") and os.path.isdir(folder):
        items = os.listdir(folder)
        if "README.md" in items:
            print(f"✅ {folder} - README present")
        if ".github" in items:
            print(f"✅ {folder} - CI config present")
