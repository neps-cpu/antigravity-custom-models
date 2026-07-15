# Changes Made to Unlock Custom Models in Antigravity IDE

This file documents all the modifications and new files created on the local system during this reverse engineering and integration task.

---

## 1. Patched IDE Javascript Bundles

The custom models UI and dropdown features were restricted to Linux OS and Google internal account domain checks. We surgically updated the following three compiled JS bundles inside the IDE installation path (`E:\D\Antigravity IDE\resources\app\out\`):

### File 1: Renderer Process Bundle
* **Path:** `E:\D\Antigravity IDE\resources\app\out\vs\workbench\workbench.desktop.main.js`
* **Patch A (Unlock UI dropdown features):**
  * **Original Line:** `d=a.osName==="linux"&&a.isGoogleInternal,h=a.isGoogleInternal`
  * **Modified Line:** `d=true,h=true`
* **Patch B (Fix startup custom model override bug):**
  * **Original Line:** `this.setSelectedModel(or(Bnc,{choice:{case:"model",value:r}}),void 0,!1)`
  * **Modified Line:** `this.setSelectedModel(or(Bnc,{choice:{case:"model",value:r}}),((_n_)=>{const t=XJt(_n_);return t?Object.values(t)[0]:void 0})(n),!1)`

### File 2: Main Process Bundle
* **Path:** `E:\D\Antigravity IDE\resources\app\out\main.js`
* **Original Line:** `f=o.osName==="linux"&&o.isGoogleInternal,p=o.isGoogleInternal`
* **Modified Line:** `f=true,p=true`

### File 3: Agent Sidebar Process Bundle
* **Path:** `E:\D\Antigravity IDE\resources\app\out\jetskiAgent\main.js`
* **Original Line:** `f=o.osName==="linux"&&o.isGoogleInternal,g=o.isGoogleInternal`
* **Modified Line:** `f=true,g=true`

---

## 2. Updated Local Database Cache

The SQLite database storing local window preferences and synced topic configurations was modified:
* **Database File:** `C:\Users\nepal\AppData\Roaming\Antigravity IDE\User\globalStorage\state.vscdb`
* **Modified Key in `ItemTable`:** `antigravityUnifiedStateSync.modelPreferences`
* **Action:** Decoded the base64 value, constructed and appended a custom `Topic` map entry mapping `"custom_models"` to a protobuf-encoded `ModelInfo` descriptor of the local proxy endpoint (`http://localhost:8000/`), and saved the updated base64 representation back to SQLite.

---

## 3. Added Global Agent Skill

A custom workspace/global agent skill was added to teach the Antigravity agent how to call the OpenRouter API endpoint programmatically via terminal shell commands:
* **Skill Directory:** `C:\Users\nepal\.gemini\config\skills\openrouter_api`
* **Skill Metadata File:** `C:\Users\nepal\.gemini\config\skills\openrouter_api\SKILL.md`
* **Query Script Helper:** `C:\Users\nepal\.gemini\config\skills\openrouter_api\scripts\query.py`
