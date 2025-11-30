# ESIA Monorepo Workspace

Environmental and Social Impact Assessment (ESIA) - Unified monorepo for all ESIA-related packages.

## Overview

This monorepo consolidates all ESIA components into a single workspace for better dependency management, code sharing, and consistent versioning.

**Location**: `M:\GitHub\esia-workspace`

## Workspace Structure

```
esia-workspace/
├── packages/
│   ├── app/              # Main web application (React + Express)
│   ├── pipeline/         # Python-based document processing pipeline
│   ├── fact-extractor/   # Fact extraction from ESIA documents
│   ├── fact-analyzer/    # Analysis and consistency checking
│   └── shared/           # Shared types, utilities, and constants
├── package.json          # Workspace root configuration
├── pnpm-workspace.yaml   # pnpm workspace definition
├── tsconfig.base.json    # Shared TypeScript configuration
└── README.md
```

## Packages

### `@esia/app`
Main web application with React frontend and Express backend for document upload and pipeline orchestration.

- **Frontend**: React 19 + Vite + TypeScript
- **Backend**: Express.js with Multer file handling
- **Location**: `packages/app`

### `@esia/pipeline`
Python-based orchestration pipeline that coordinates document processing through multiple stages.

- **Language**: Python
- **Location**: `packages/pipeline`
- **Key Files**:
  - `run-esia-pipeline.py` - Main orchestrator
  - `config.py` - Pipeline configuration

### `@esia/fact-extractor`
Extracts domain-specific facts and information from ESIA documents using pattern matching and archetype-based extraction.

- **Language**: Python
- **Location**: `packages/fact-extractor`
- **Key File**: `esia_extractor.py`

### `@esia/fact-analyzer`
Analyzes extracted facts for consistency, compliance issues, and generates comprehensive analysis reports.

- **Language**: Python
- **Location**: `packages/fact-analyzer`
- **Key Files**:
  - `esia_analyzer/` - Analysis modules
  - `analyze_esia_v2.py` - Analysis orchestrator

### `@esia/shared`
Shared TypeScript types, utility functions, and constants used across Node.js packages.

- **Language**: TypeScript
- **Location**: `packages/shared`
- **Exports**:
  - `@esia/shared` - All exports
  - `@esia/shared/types` - Type definitions
  - `@esia/shared/utils` - Utility functions

## Setup Instructions

### Prerequisites

- **Node.js** 18+
- **pnpm** 8+ (or npm/yarn)
- **Python** 3.9+ (for pipeline packages)

### Installation

1. **Install workspace dependencies**:
   ```bash
   cd M:\GitHub\esia-workspace
   pnpm install
   ```

2. **Install Python dependencies** (for each Python package):
   ```bash
   cd packages/pipeline
   pip install -r requirements.txt

   cd ../fact-extractor
   pip install -r requirements.txt

   cd ../fact-analyzer
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` files to `.env` in each package
   - Configure API keys and settings as needed

## Development

### Start all services
```bash
pnpm dev
```

### Start specific services
```bash
pnpm dev:app        # Run only the web app
pnpm dev:pipeline   # Run only pipeline service
```

### Build all packages
```bash
pnpm build
```

### Run tests
```bash
pnpm test
```

## Architecture

### Data Flow

```
User Browser
    ↓
React Frontend (port 3000)
    ↓
Express Backend (port 5000)
    ↓
Python Pipeline
    ├→ Docling Chunking
    ├→ Fact Extraction
    └→ Analysis & Consistency Check
    ↓
Output Storage & Frontend Display
```

### Communication

- **Frontend ↔ Backend**: REST API (`/api/` endpoints)
- **Backend ↔ Python**: Subprocess spawning with status polling
- **Status Tracking**: In-memory execution state with cleanup

## Package Dependencies

### Inter-package Dependencies

```
app (frontend + backend)
  └→ shared (types, utils)

pipeline (orchestrator)
  ├→ fact-extractor
  └→ fact-analyzer

fact-extractor (extraction logic)
  └→ shared (if needed for types)

fact-analyzer (analysis logic)
  └→ shared (if needed for types)
```

### Using Shared Package

In any Node.js package:

```typescript
import { sanitizeFilename, generateExecutionId } from '@esia/shared';
import type { PipelineExecution, ExtractedFact } from '@esia/shared';
```

In `package.json`:
```json
{
  "dependencies": {
    "@esia/shared": "workspace:*"
  }
}
```

## Configuration

### Workspace Configuration

- **`package.json`**: Root scripts, workspace definition
- **`pnpm-workspace.yaml`**: Package catalog and version management
- **`tsconfig.base.json`**: Shared TypeScript compiler options and path aliases

### Package-Level Configuration

Each package maintains its own:
- `package.json` - Dependencies specific to that package
- `tsconfig.json` - Extends `tsconfig.base.json`
- `.env` files - Package-specific configuration
- Config files (e.g., `vite.config.ts`, `pipeline.config.js`)

## Scripts Reference

### Root Workspace Scripts

| Command | Description |
|---------|-------------|
| `pnpm install` | Install all dependencies |
| `pnpm dev` | Run all packages in dev mode |
| `pnpm dev:app` | Run web app only |
| `pnpm dev:pipeline` | Run pipeline service only |
| `pnpm build` | Build all packages |
| `pnpm build:app` | Build app package only |
| `pnpm test` | Run tests in all packages |
| `pnpm lint` | Lint all packages |
| `pnpm clean` | Remove all `dist` and `node_modules` |

### Package-Specific Scripts

Navigate to individual packages and run their scripts:

```bash
cd packages/app
pnpm dev              # Start frontend and backend
pnpm run dev:frontend # Frontend only
pnpm run dev:server   # Backend only
pnpm build            # Build for production

cd packages/pipeline
python run-esia-pipeline.py <pdf_path>
```

## Environment Variables

### App Package (`.env.local`)
```
GEMINI_API_KEY=your_api_key
```

### Pipeline Package (`.env`)
```
# Pipeline configuration
API_KEY=your_key
```

### Fact Extractor (`.env`)
```
# Extraction configuration
```

### Fact Analyzer (`.env`)
```
# Analysis configuration
```

## Migration From Old Structure

**Old locations** → **New locations**:
- `M:\GitHub\esia-ai` → `M:\GitHub\esia-workspace\packages\app`
- `M:\GitHub\esia-pipeline` → `M:\GitHub\esia-workspace\packages\pipeline`
- `M:\GitHub\esia-fact-extractor` → `M:\GitHub\esia-workspace\packages\fact-extractor`
- `M:\GitHub\esia-fact-analyzer` → `M:\GitHub\esia-workspace\packages\fact-analyzer`

**Updating import paths**:

Old:
```javascript
const pipeline = require('../esia-pipeline');
```

New:
```typescript
import type { PipelineExecution } from '@esia/shared';
```

## Troubleshooting

### Dependencies Not Resolving

```bash
# Clear and reinstall
pnpm clean
pnpm install
```

### Port Conflicts

- **Frontend**: 3000 (configurable in `vite.config.ts`)
- **Backend**: 5000 (configurable in `server.js`)
- **Python Pipeline**: Check service port configuration

### Python Environment Issues

```bash
# Create isolated virtual environment per package
cd packages/pipeline
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Performance Tips

1. **Use workspace filtering** to run specific packages:
   ```bash
   pnpm --filter @esia/app install
   pnpm --filter @esia/pipeline dev
   ```

2. **Keep shared utilities lightweight** to avoid circular dependencies

3. **Use path aliases** in `tsconfig.base.json` instead of relative imports

## Contributing

1. Create feature branch: `git checkout -b feature/description`
2. Make changes to relevant packages
3. Test across packages: `pnpm test`
4. Commit with workspace context: `git commit -m "feat(app): add feature"`
5. Push and create PR

## Future Improvements

- [ ] Add automated testing across packages
- [ ] Set up CI/CD pipeline for monorepo
- [ ] Create shared documentation site
- [ ] Implement version synchronization
- [ ] Add deployment automation
- [ ] Create shared component library

## License

[Add your license here]

## Support

For issues or questions about:
- **App/Frontend**: See `packages/app/README.md`
- **Pipeline**: See `packages/pipeline/README.md`
- **Extraction**: See `packages/fact-extractor/CLAUDE.md`
- **Analysis**: See `packages/fact-analyzer/claude.md`
