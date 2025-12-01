# Python 3.12 Quick Activation Guide

## Option 1: PowerShell (Recommended)

### Quick One-Liner
```powershell
cd M:\GitHub\esia-workspace\packages\pipeline; .\activate-py312.ps1
```

### Or from PowerShell Profile (Permanent Alias)

Add this to your PowerShell profile to create a global `activate-py312` command:

```powershell
# Edit PowerShell profile
notepad $PROFILE

# Add this line to the profile file:
function activate-py312 { & 'M:\GitHub\esia-workspace\packages\pipeline\venv312\Scripts\Activate.ps1' }
```

Then reload your profile:
```powershell
. $PROFILE
```

Now you can activate from anywhere by just typing:
```powershell
activate-py312
```

## Option 2: Command Prompt (cmd.exe)

### Quick One-Liner
```cmd
cd M:\GitHub\esia-workspace\packages\pipeline && activate-py312.bat
```

### Or Create a Batch Shortcut
Create a batch file in a folder in your PATH (e.g., `C:\Scripts\`) named `activate-py312.bat`:
```batch
@echo off
"M:\GitHub\esia-workspace\packages\pipeline\venv312\Scripts\activate.bat"
```

Then call it from anywhere:
```cmd
activate-py312
```

## Option 3: Direct Path (No Script Needed)

```powershell
# PowerShell
& 'M:\GitHub\esia-workspace\packages\pipeline\venv312\Scripts\Activate.ps1'
```

```cmd
REM Command Prompt
"M:\GitHub\esia-workspace\packages\pipeline\venv312\Scripts\activate.bat"
```

## Verify Activation

After activation, verify you're using Python 3.12:

```powershell
python --version
# Should output: Python 3.12.7

# Check venv312 is active (should show venv312 in prompt)
# Example: (venv312) PS M:\GitHub\esia-workspace\packages\pipeline>
```

## Quick Commands After Activation

```powershell
# Check Python version
python --version

# Check GPU support
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Run pipeline
python run-esia-pipeline.py data/pdfs/document.pdf --steps 1,2,3

# Or use the convenience scripts
.\run-pipeline.ps1 data/pdfs/document.pdf --steps 1 --verbose
```

## Deactivate When Done

```powershell
deactivate
```

---

## Recommended Setup

1. **Add to PowerShell Profile** (one-time setup):
   ```powershell
   notepad $PROFILE
   # Add: function activate-py312 { & 'M:\GitHub\esia-workspace\packages\pipeline\venv312\Scripts\Activate.ps1' }
   . $PROFILE
   ```

2. **Then use anytime**:
   ```powershell
   activate-py312
   ```

This is the most convenient way to activate Python 3.12 from any PowerShell window.
