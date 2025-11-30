# Migration Guide: From Individual Repos to Monorepo

This guide helps you transition from the old individual repository structure to the new monorepo workspace.

## What Changed

### Old Structure
```
M:\GitHub\
├── esia-ai/              (main app)
├── esia-pipeline/        (pipeline)
├── esia-fact-extractor/  (extraction)
└── esia-fact-analyzer/   (analysis)
```

### New Structure
```
M:\GitHub\
└── esia-workspace/
    └── packages/
        ├── app/
        ├── pipeline/
        ├── fact-extractor/
        ├── fact-analyzer/
        └── shared/
```

## Benefits of the Monorepo

✅ **Unified Dependency Management** - Single `pnpm-lock.yaml` for consistent versions
✅ **Code Sharing** - Shared utilities package with common functions
✅ **Easier Refactoring** - Move code between packages with clear boundaries
✅ **Atomic Commits** - Track changes across all packages in single commit
✅ **Simplified CI/CD** - One pipeline for all packages
✅ **Clear Dependency Graph** - Easy to see inter-package relationships

## Migration Steps

### For Developers

1. **Update local path in git**:
   ```bash
   # Remove old folders from git tracking
   git rm --cached -r ../esia-ai ../esia-pipeline ../esia-fact-extractor ../esia-fact-analyzer

   # Navigate to new workspace
   cd M:\GitHub\esia-workspace
   ```

2. **Install dependencies**:
   ```bash
   pnpm install
   ```

3. **Update any git remotes**:
   ```bash
   git remote set-url origin https://github.com/your-org/esia-workspace.git
   ```

### For Import Paths

#### JavaScript/TypeScript

**Old (relative imports):**
```javascript
// In esia-ai/server.js
const pipeline = require('../esia-pipeline/run-esia-pipeline.py');
import type { Execution } from '../esia-fact-analyzer/types';
```

**New (workspace imports):**
```javascript
// In packages/app/server.js
import { PipelineExecution } from '@esia/shared';
// No need to import from other packages directly - use shared types
```

#### Python

No changes needed - Python packages remain independent and are executed as subprocesses.

### For Configuration

#### Environment Variables

**Before:**
- `esia-ai/.env.local`
- `esia-pipeline/.env`
- `esia-fact-extractor/.env`
- `esia-fact-analyzer/.env`

**After:** (same structure, same file contents)
- `packages/app/.env.local`
- `packages/pipeline/.env`
- `packages/fact-extractor/.env`
- `packages/fact-analyzer/.env`

Copy your existing `.env` files to the new locations.

#### Build Configuration

**TypeScript paths in `vite.config.ts`:**

**Old:**
```typescript
export default {
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    }
  }
};
```

**New:**
```typescript
export default {
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@esia/shared': resolve(__dirname, '../../shared/src'),
    }
  }
};
```

Or just use the workspace import:
```typescript
import type { PipelineExecution } from '@esia/shared';
```

### For Documentation

#### Updating README References

**Old:**
```markdown
See [esia-pipeline README](../esia-pipeline/README.md)
```

**New:**
```markdown
See [Pipeline README](packages/pipeline/README.md)
```

#### Documentation Location

Keep documentation where it was:
- `packages/app/README.md`
- `packages/pipeline/README.md`
- `packages/fact-extractor/CLAUDE.md`
- `packages/fact-analyzer/claude.md`

## Workspace Scripts Usage

### Running All Services
```bash
cd M:\GitHub\esia-workspace
pnpm dev
```

### Running Individual Services
```bash
pnpm dev:app        # Frontend & backend only
pnpm dev:pipeline   # Just pipeline (if applicable)
```

### Filtering Packages
```bash
# Install only app dependencies
pnpm --filter @esia/app install

# Run dev for specific package
pnpm --filter @esia/app dev

# Build only one package
pnpm --filter @esia/fact-extractor build
```

## Troubleshooting Migration Issues

### Issue: "Cannot find module '@esia/shared'"

**Solution:** Make sure `shared` is listed in workspace configuration:
```json
// package.json
"workspaces": ["packages/*"]
```

Then reinstall:
```bash
pnpm install
```

### Issue: Python scripts in old location

**Solution:** Update import path in Node.js code:

**Old:**
```javascript
spawn('python', ['../esia-pipeline/run-esia-pipeline.py']);
```

**New:**
```javascript
spawn('python', ['./packages/pipeline/run-esia-pipeline.py']);
// or from app perspective:
spawn('python', ['../../pipeline/run-esia-pipeline.py']);
```

### Issue: Port conflicts

Check if services are trying to use same ports:
- Frontend (Vite): 3000 - Configure in `vite.config.ts`
- Backend (Express): 5000 - Configure in `server.js`

### Issue: Git history

**Old commits are in separate repositories** - You'll need to:

1. Keep old repos as reference
2. Start fresh git history in monorepo:
   ```bash
   cd esia-workspace
   git init
   git add .
   git commit -m "Initial commit: ESIA monorepo migration"
   ```

3. Or merge histories using git subtree/submodule (advanced)

## Updating CI/CD

### GitHub Actions

**Old workflow (separate repos):**
```yaml
# Each repo has its own workflow
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
```

**New workflow (monorepo):**
```yaml
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: [app, pipeline, fact-extractor, fact-analyzer]
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: pnpm --filter @esia/${{ matrix.package }} test
```

## Keeping Old Repositories

We recommend **archiving** old repositories rather than deleting:

1. Make repo private (if using GitHub)
2. Add note in README: "This repository has been merged into [esia-workspace](link)"
3. Don't delete - keep for history reference

## Quick Reference

| Task | Command |
|------|---------|
| Install all deps | `pnpm install` |
| Dev mode (all) | `pnpm dev` |
| Dev mode (app only) | `pnpm dev:app` |
| Build all | `pnpm build` |
| Build one package | `pnpm --filter @esia/app build` |
| Add dep to shared | `pnpm --filter @esia/shared add lodash` |
| Test all | `pnpm test` |
| Clean everything | `pnpm clean` |

## Support

For migration questions:
1. Check individual package READMEs in `packages/*/README.md`
2. Review workspace `README.md` at root
3. Check package-specific documentation files

## Rollback (if needed)

Keep old repositories available for 1-2 weeks before archiving, in case you need to revert.

To revert to old structure:
1. Go back to old repository directories
2. Update git remotes to point to old repos
3. Delete the monorepo workspace (or keep as backup)

However, we recommend staying with monorepo - the benefits outweigh the cost of migration.
