# Antigravity IDE - Custom Model Unlock & OpenRouter API Integration
### Created by Neps

This repository contains the tools, scripts, and configurations to unlock **Custom Model Selection** in the Google Antigravity IDE on Windows, and integrate any custom model via **OpenRouter** (`https://openrouter.ai/api/v1`) without any token limits.

---

## Repository Structure

* **`patch_custom_models.py`**: A python script that bypasses OS and account validation checks in the Antigravity IDE UI by surgically patching the compiled Javascript bundles in the installation path.
* **`save_custom_model.py`**: A database tool that directly serializes and writes the custom model configuration into the local SQLite settings database (`state.vscdb`) to bypass cloud settings sync blocks.
* **`local_proxy.py`**: A lightweight local proxy server that intercepts OpenAI-compatible request payloads from the IDE, rewrites the model parameter to the OpenRouter format, injects any custom authorization headers/API keys, and forwards them to the endpoint URL.
* **`skills/openrouter_api/`**:
  * **`SKILL.md`**: Custom agent skill metadata that registers the API globally.
  * **`scripts/query.py`**: A lightweight Python wrapper client to query the OpenRouter endpoint.

---

## Step-by-Step Instructions

### Step 1: Run the Local Proxy Server (Handling Custom API Keys & Base URLs)
Because the IDE UI does not provide an "API Key" input field for custom Evergreen/BYOM models, running a local proxy allows you to inject any header or key transparently:

1. Open `local_proxy.py` and configure your API key and base URL at the top:
   ```python
   PORT = 8000
   TARGET_URL = "https://openrouter.ai/api/v1"
   API_KEY = "YOUR_OPENROUTER_API_KEY"
   REWRITE_MODEL = "anthropic/claude-3.5-sonnet"
   ```
2. Start the local server:
   ```bash
   python local_proxy.py
   ```
This will listen on `http://localhost:8000` and automatically forward requests to OpenRouter!

### Step 2: Patch the Antigravity IDE (Unlock Custom Model Dropdown)
By default, the Antigravity IDE blocks the Custom Model UI on Windows and non-internal accounts. 

1. Ensure the paths inside `patch_custom_models.py` point to your IDE installation folder (e.g. `E:\D\Antigravity IDE`).
2. Run the patcher script:
   ```bash
   python patch_custom_models.py
   ```
3. Open the Antigravity IDE, open the Command Palette (`Ctrl+Shift+P`), and run **`Developer: Reload Window`** to reload the patched bundles into memory. You will now see the `Custom Models` header and the `+` (Add Custom Model) option in your dropdown!

### Step 3: Configure and Save the Model Config
To persist your custom model settings without being blocked by cloud settings sync validation:

1. Open `save_custom_model.py` and set your custom model variables at the top. Since you are using the proxy server, set `BASE_URL` to `http://localhost:8000/`:
   ```python
   MODEL_LABEL = "OpenRouter-Claude"
   BASE_URL = "http://localhost:8000/"  # Points to local_proxy.py
   MAX_TOKENS = 1000000                 # Large value (no token limits)
   ```
2. Close the IDE or prepare to reload, then run the database script to write it into `state.vscdb`:
   ```bash
   python save_custom_model.py
   ```
3. Reload your IDE window (`Developer: Reload Window`). The **OpenRouter-Claude** custom model will be pre-loaded and selected in the model dropdown list, routing requests through your proxy server without any token limits!

---

## How to Upload to GitHub

Follow these steps to upload this folder to your GitHub account:

### Option A: Using the Command Line (Git)

1. Open **Command Prompt** or **PowerShell** and navigate to this folder:
   ```bash
   cd "C:\Users\nepal\Desktop\for github"
   ```
2. Initialize the Git repository:
   ```bash
   git init
   ```
3. Add all files to staging:
   ```bash
   git add .
   ```
4. Commit the files:
   ```bash
   git commit -m "Initial commit by Neps - Unlocking Custom Models in Antigravity IDE"
   ```
5. Create a new repository on [GitHub](https://github.com/new).
6. Copy the remote repository URL and link it (replace with your repository link):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   ```
7. Rename the default branch to `main`:
   ```bash
   git branch -M main
   ```
8. Push to GitHub:
   ```bash
   git push -u origin main
   ```

---

### Option B: Using the GitHub Website (No Terminal needed)

1. Go to [GitHub](https://github.com) and click **New Repository**.
2. Give it a name (e.g. `antigravity-custom-models`) and click **Create repository**.
3. On the setup screen, click the **"uploading an existing file"** link.
4. Drag and drop all the files and folders from the `for github` folder on your Desktop into the upload area.
5. Click **Commit changes** at the bottom.
