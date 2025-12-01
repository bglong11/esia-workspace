# ESIA Fact Analyzer - Documentation Index

Complete guide to all documentation files and how to use them.

---

## Quick Start

**New to this project?** Start here:

1. **First time setup:** Read [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. **What it does:** Read [README.md](README.md)
3. **Run your first analysis:** See examples in [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## Documentation Files

### 📄 Core Documentation

#### [README.md](README.md)
**What it is:** Main project documentation
**Contents:**
- Project overview and features
- Installation instructions
- Quick start guide
- Input/output formats
- Parameter reference
- Configuration & customization
- Troubleshooting

**Read if:** You want a comprehensive understanding of the tool

#### [SKILL_v2.md](SKILL_v2.md)
**What it is:** Feature documentation for AI/skill integration
**Contents:**
- What's new in v2.0
- Complete workflow guide
- Feature descriptions
- Parameter contexts (17 types)
- Unit conversions (80+ conversions)
- Gap analysis categories (30+ items)

**Read if:** You're integrating this as an AI skill or need detailed feature info

### 📋 Setup & Usage

#### [SETUP_GUIDE.md](SETUP_GUIDE.md)
**What it is:** Step-by-step setup and usage guide
**Contents:**
- Quick start (3 steps)
- File structure explanation
- Command examples (basic to advanced)
- Parameter reference table
- Error messages & solutions
- Input file formats
- Output file descriptions
- Workflow examples
- Troubleshooting guide

**Read if:** You need help setting up or using the tool

#### [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)
**What it is:** Technical details of the CLI refactoring
**Contents:**
- What changed (before/after)
- CLI parameter changes
- Usage examples
- Implementation details
- File discovery logic
- Error handling
- Console output changes
- Migration path for existing users

**Read if:** You want to understand the CLI redesign or migrating from older version

### 📚 Development & Analysis

#### [claude.md](claude.md)
**What it is:** Developer context and architecture guide
**Contents:**
- Project genesis and philosophy
- Architecture overview
- Core class structure
- Implementation details
- Key components
- How to add new features
- Debugging tips
- Future enhancement ideas
- Contributing guidelines

**Read if:** You're developing or extending the tool

#### [ANALYSIS_EXAMPLE.md](ANALYSIS_EXAMPLE.md)
**What it is:** Real-world analysis walkthrough
**Contents:**
- Complete example from actual ESIA document
- Consistency issues explained (11 examples)
- Unit standardization issues (4 examples)
- Content gap analysis (all 6 sections)
- Detailed interpretations
- Risk assessment
- Recommendations for each finding

**Read if:** You want to see how the tool works on real data

### 🔄 Change Management

#### [CHANGELOG.md](CHANGELOG.md)
**What it is:** Version changelog
**Contents:**
- v2.0.1: IFC Threshold Compliance removal
- v2.0: Initial release features
- Removed features documentation
- Updated files list
- Backward compatibility notes

**Read if:** You need to understand what changed between versions

#### [REMOVAL_SUMMARY.md](REMOVAL_SUMMARY.md)
**What it is:** Technical details of IFC threshold removal
**Contents:**
- Exactly what was removed
- Why it was removed
- Files modified
- Data structure changes
- Backward compatibility impact
- Re-enablement instructions

**Read if:** You need to understand the threshold compliance removal

#### [COMPLETION_REPORT.md](COMPLETION_REPORT.md)
**What it is:** Completion report for threshold removal
**Contents:**
- Task summary
- What was changed
- Testing & verification results
- Quality assurance checklist
- Summary of impact

**Read if:** You want overview of the removal project

---

## Documentation by Use Case

### "I'm new to this tool"
1. Start: [SETUP_GUIDE.md](SETUP_GUIDE.md) (Quick Start section)
2. Learn: [README.md](README.md) (What It Does section)
3. Try: [SETUP_GUIDE.md](SETUP_GUIDE.md) (Command Examples)
4. Deep dive: [ANALYSIS_EXAMPLE.md](ANALYSIS_EXAMPLE.md)

### "I want to use the tool"
1. Setup: [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Run: Follow examples in SETUP_GUIDE.md
3. Understand results: [ANALYSIS_EXAMPLE.md](ANALYSIS_EXAMPLE.md)
4. Reference: [README.md](README.md) for features

### "I'm extending/developing the tool"
1. Understand: [claude.md](claude.md) (Architecture)
2. Reference: [README.md](README.md) (Features)
3. Code: [analyze_esia_v2.py](analyze_esia_v2.py)
4. Contribute: [claude.md](claude.md) (Contributing Guidelines)

### "I'm upgrading from an older version"
1. Changes: [CHANGELOG.md](CHANGELOG.md)
2. Migration: [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) (Migration Path)
3. New setup: [SETUP_GUIDE.md](SETUP_GUIDE.md)

### "Something is broken"
1. Check: [SETUP_GUIDE.md](SETUP_GUIDE.md) (Troubleshooting)
2. Understand: [README.md](README.md) (Troubleshooting)
3. Debug: [claude.md](claude.md) (Debugging Tips)

---

## File Organization

```
esia-fact-analyzer/
├── INDEX.md                          ← You are here
├── README.md                         ← Start here
├── SETUP_GUIDE.md                    ← How to use
├── SKILL_v2.md                       ← Features
├── claude.md                         ← Development
├── ANALYSIS_EXAMPLE.md               ← Real example
├── REFACTORING_SUMMARY.md            ← CLI changes
├── CHANGELOG.md                      ← Version history
├── REMOVAL_SUMMARY.md                ← Threshold removal
├── COMPLETION_REPORT.md              ← Project completion
│
├── analyze_esia_v2.py                ← Main script
├── data/
│   ├── analysis_inputs/              ← Input folder
│   │   ├── chunks.jsonl
│   │   └── meta.json
│   └── analysis_outputs/             ← Output folder
│       ├── document_review.html
│       └── document_review.xlsx
└── [reference data, samples, etc.]
```

---

## Quick Reference

### Most Important Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Complete project documentation |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | How to set up and run |
| [ANALYSIS_EXAMPLE.md](ANALYSIS_EXAMPLE.md) | See it in action |
| [SKILL_v2.md](SKILL_v2.md) | Feature reference |

### For Developers

| File | Purpose |
|------|---------|
| [claude.md](claude.md) | Architecture & design |
| [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) | CLI implementation |
| [REMOVAL_SUMMARY.md](REMOVAL_SUMMARY.md) | Technical changes |
| [analyze_esia_v2.py](analyze_esia_v2.py) | Source code |

### For Users

| File | Purpose |
|------|---------|
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Getting started |
| [README.md](README.md) | Features & parameters |
| [ANALYSIS_EXAMPLE.md](ANALYSIS_EXAMPLE.md) | How to interpret results |
| [SKILL_v2.md](SKILL_v2.md) | Analysis details |

---

## How to Navigate

### By Topic

**Using the Tool:**
- Quick start: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Features: [README.md](README.md)
- Examples: [ANALYSIS_EXAMPLE.md](ANALYSIS_EXAMPLE.md)

**Understanding the Code:**
- Architecture: [claude.md](claude.md)
- Implementation: [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)
- Changes: [CHANGELOG.md](CHANGELOG.md)

**Troubleshooting:**
- Setup issues: [SETUP_GUIDE.md](SETUP_GUIDE.md) - Troubleshooting
- Feature questions: [README.md](README.md)
- Code problems: [claude.md](claude.md) - Debugging Tips

### By Document Type

**Quick Start:**
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 3-minute quickstart

**How-To Guides:**
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Setup & usage
- [SKILL_v2.md](SKILL_v2.md) - Workflow guide
- [README.md](README.md) - Configuration

**References:**
- [SKILL_v2.md](SKILL_v2.md) - Features & parameters
- [README.md](README.md) - Comprehensive reference
- [ANALYSIS_EXAMPLE.md](ANALYSIS_EXAMPLE.md) - Real examples

**Technical:**
- [claude.md](claude.md) - Architecture
- [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) - Implementation
- [REMOVAL_SUMMARY.md](REMOVAL_SUMMARY.md) - Technical details

**Historical:**
- [CHANGELOG.md](CHANGELOG.md) - Version changes
- [COMPLETION_REPORT.md](COMPLETION_REPORT.md) - Project status

---

## Key Concepts

### Input Folder (`./data/analysis_inputs/`)
- **chunks.jsonl** (required) - Extracted facts from ESIA document
- **meta.json** (optional) - Document metadata

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for format details.

### Output Folder (`./data/analysis_outputs/`)
- **{name}_review.html** - Interactive dashboard
- **{name}_review.xlsx** - Detailed Excel report

See [README.md](README.md) for output interpretation.

### Analysis Features
- **Fact Categorization** - 11 ESIA categories
- **Consistency Checking** - 17 parameter contexts
- **Unit Standardization** - 80+ unit conversions
- **Gap Analysis** - 30+ expected content items

See [SKILL_v2.md](SKILL_v2.md) for detailed feature info.

---

## Documentation Maintenance

**Last Updated:** November 28, 2024
**Version:** 2.0.1
**Total Docs:** 10 files
**Total Pages:** ~100+ pages of documentation

**Notable Updates:**
- ✅ CLI refactored (Nov 28)
- ✅ Threshold compliance removed (Nov 27)
- ✅ Context-aware intelligence explained (Nov 27)
- ✅ README created (Nov 27)

---

## Getting Help

### For Usage Questions
→ [SETUP_GUIDE.md](SETUP_GUIDE.md)

### For Feature Details
→ [SKILL_v2.md](SKILL_v2.md) or [README.md](README.md)

### For Development
→ [claude.md](claude.md)

### For Examples
→ [ANALYSIS_EXAMPLE.md](ANALYSIS_EXAMPLE.md)

### For Troubleshooting
→ [SETUP_GUIDE.md](SETUP_GUIDE.md) - Troubleshooting section

---

**This document provides a map to all documentation. Start with [SETUP_GUIDE.md](SETUP_GUIDE.md) if you're new!**
