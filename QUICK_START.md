# ESIA Monorepo - Quick Start Guide

## 🎯 Fastest Way to Get Started

### 1. Navigate to Workspace
```bash
cd M:\GitHub\esia-workspace
```

### 2. Install Dependencies
```bash
# Using pnpm (recommended)
pnpm install

# Or npm
npm install
```

### 3. Start Developing
```bash
# Start all services (frontend + backend)
pnpm dev

# Or start specific service
pnpm dev:app
```

### 4. Open in Browser
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000

---

## 📁 Monorepo Structure at a Glance

```
esia-workspace/
├── packages/
│   ├── app/              (React frontend + Express backend)
│   ├── pipeline/         (Python pipeline orchestrator)
│   ├── fact-extractor/   (Python fact extraction)
│   ├── fact-analyzer/    (Python analysis)
│   └── shared/           (TypeScript shared utilities)
├── README.md             (Full documentation)
├── SETUP_SUMMARY.md      (Setup details)
├── MIGRATION_GUIDE.md    (Code migration help)
├── package.json          (Workspace config)
└── pnpm-workspace.yaml   (Package manager config)
```

---

## 🔧 Common Commands

```bash
# Installation
pnpm install                    # Install everything
pnpm --filter @esia/app install # Install specific package

# Development
pnpm dev                        # All services
pnpm dev:app                    # App only

# Building
pnpm build                      # Build all packages
pnpm build:app                  # Build specific package

# Cleanup
pnpm clean                      # Remove dist/node_modules
```

---

## 📝 What Each Package Does

### `packages/app`
**React + Express web application**
- Port 3000: React frontend (Vite)
- Port 5000: Express backend
- Handles PDF upload and pipeline orchestration

### `packages/pipeline`
**Python pipeline orchestrator**
- Coordinates document processing workflow
- Main file: `run-esia-pipeline.py`
- Runs as subprocess from backend

### `packages/fact-extractor`
**Fact extraction engine**
- Extracts structured information from documents
- Pattern matching and archetype-based extraction
- Main file: `esia_extractor.py`

### `packages/fact-analyzer`
**Analysis and consistency checking**
- Analyzes extracted facts
- Identifies issues and inconsistencies
- Generates reports
- Main file: `analyze_esia_v2.py`

### `packages/shared`
**Shared utilities (TypeScript)**
- Common types: `PipelineExecution`, `ExtractedFact`, etc.
- Utility functions: `sanitizeFilename()`, `generateExecutionId()`, etc.
- Import: `import { ... } from '@esia/shared'`

---

## 🌐 Environment Setup

### Create `.env.local` for app
```bash
# M:\GitHub\esia-workspace\packages\app\.env.local
GEMINI_API_KEY=your_key_here
```

### Create `.env` for Python packages
```bash
# M:\GitHub\esia-workspace\packages\pipeline\.env
API_KEY=your_key_here
```

---

## 🐍 Python Setup

If Python packages need separate virtual environments:

```bash
# For each Python package
cd packages/pipeline
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎓 Learning Path

1. **Understand the structure**: Read [README.md](README.md)
2. **Check individual packages**: See `packages/*/README.md`
3. **Migration help**: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
4. **Detailed setup**: See [SETUP_SUMMARY.md](SETUP_SUMMARY.md)

---

## ✅ Verification Checklist

- [ ] Can navigate to `M:\GitHub\esia-workspace`
- [ ] `pnpm install` completes without errors
- [ ] `pnpm dev` starts services successfully
- [ ] Frontend loads at http://localhost:3000
- [ ] Backend responds at http://localhost:5000/health

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 3000/5000 in use | Kill process or change port in config |
| "Cannot find pnpm" | Install: `npm install -g pnpm` |
| Dependencies not found | Run: `pnpm install` again |
| Python errors | Check Python 3.9+, run `pip install -r requirements.txt` |
| Import errors | Verify `@esia/shared` imports in `tsconfig.base.json` |

---

## 📞 Getting Help

1. **Package-specific issues**: Check `packages/*/README.md`
2. **Code migration**: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
3. **Setup issues**: See [SETUP_SUMMARY.md](SETUP_SUMMARY.md)
4. **Architecture**: See [README.md](README.md)

---

**That's it! Happy coding! 🚀**
