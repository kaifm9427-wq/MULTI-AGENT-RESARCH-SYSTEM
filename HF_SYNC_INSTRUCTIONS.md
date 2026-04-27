# HuggingFace Space - GitHub Sync Instructions

## Current Status

❌ **NOT SYNCED**: Your HuggingFace Space has the OLD code  
✅ **GitHub**: Has the LATEST fixed code

## Evidence

**Old Code (Currently on HF Space):**
```javascript
const API_BASE = 'http://localhost:8000/api';  // Hardcoded localhost!
```

**New Code (On GitHub, not deployed):**
```javascript
const API_BASE = window.location.origin + '/api';  // Dynamic URL!
```

## How to Sync

### Method 1: Manual Sync (Recommended - 2 minutes)

1. Go to: https://huggingface.co/spaces/kaifyyy06/research-mind/settings
2. Scroll to "Repository" section
3. Click "Sync with repository" button
4. Or, click the three dots (⋯) → "Restart space"
5. Wait 1-2 minutes for rebuild
6. Hard refresh browser (Cmd/Ctrl + Shift + R)

### Method 2: Force Rebuild

1. Go to Space settings
2. Click "Settings" → "Repository"
3. Temporarily change any setting and save
4. Change it back to force a rebuild
5. Space will auto-sync and restart

### Method 3: Reconnect Repository

1. Go to: https://huggingface.co/spaces/kaifyyy06/research-mind/settings
2. Under "Repository":
   - URL: https://github.com/kaifm9427-wq/MULTI-AGENT-RESARCH-SYSTEM
   - Branch: main
   - Private repo: No
3. Click "Save"
4. Wait for sync and rebuild

## What Will Be Updated

After sync, you'll get:
✅ Fixed API_BASE (dynamic instead of hardcoded)
✅ Enhanced error handling
✅ Better DOM initialization
✅ Improved console logging
✅ Cleaned up project structure
✅ Better HF Spaces detection

## Verification After Sync

1. Hard refresh: Cmd/Ctrl + Shift + R
2. Open DevTools: F12
3. Go to Console tab
4. You should see:
   ```
   [ResearchMind] Initializing app...
   [ResearchMind] API_BASE: https://kaifyyy06-research-mind.hf.space/api
   [ResearchMind] ✅ All DOM elements found
   ```

5. Then try a query and check for:
   ```
   [ResearchMind] Starting research for: [query]
   [ResearchMind] Response status: 200
   ```

## If Sync Doesn't Work Automatically

Contact HuggingFace support or:
1. Delete the current Space
2. Create a new Space linked to: https://github.com/kaifm9427-wq/MULTI-AGENT-RESARCH-SYSTEM

---

**Status**: Updated code is on GitHub and ready to deploy  
**Next Step**: Manually sync the repository in HF Space settings
