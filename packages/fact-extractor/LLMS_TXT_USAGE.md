# Using llms.txt for Claude Code Understanding

## Overview

The `llms.txt` file in the project root is a comprehensive reference document for DSPy framework concepts and LLM integration patterns. Claude Code can use this file to better understand the DSPy technology that powers this ESIA Fact Extractor.

## File Location

```
M:\GitHub\esia-fact-extractor\llms.txt
```

## What's Inside llms.txt

The file contains detailed documentation on:

1. **DSPy Framework Architecture**
   - Signatures: Type-safe interfaces for LM interactions
   - Modules: Composable building blocks
   - Predictors: Components using signatures for structured I/O
   - Optimizers: Tools for automatic prompt optimization
   - Adapters: Integration with various LM providers

2. **Language Model Programming**
   - Compositional programming patterns
   - Multi-step reasoning with ChainOfThought
   - Prompt optimization techniques
   - In-context learning approaches

3. **Practical Examples**
   - Creating signatures for LLM I/O
   - Building modules from signatures
   - Configuring different LLM providers
   - Development workflows

4. **Best Practices**
   - Type-safe LLM interfaces
   - Modular system design
   - Error handling patterns
   - Integration strategies

## How Claude Code Uses It

When working on this project, Claude Code can:

1. **Reference DSPy Patterns**: Look up signature definitions, module structures, and reasoning patterns used in the ESIA extractor

2. **Understand Architecture**: Get context on why the project uses DSPy's ChainOfThought for fact extraction

3. **Propose Enhancements**: Make informed suggestions about:
   - Improving the `FactExtraction` signature
   - Adding new DSPy modules
   - Optimizing extraction logic
   - Integrating new LLM providers

4. **Troubleshoot Issues**: Reference best practices for DSPy-related problems

## Key Sections to Reference

### For Signature Enhancement
See "Signatures" section to understand how to improve the current `FactExtraction` signature used in `esia_extractor.py`

### For Module Design
See "Building a Module" section for patterns to refactor the `FactExtractor` class

### For Multi-LLM Support
See "Configuration" and "Adapters" sections to understand how to support multiple LLM providers (not just Ollama)

### For Optimization
See "Automatic Prompt Optimization" section to understand how DSPy can optimize extraction prompts

## Example Usage

When Claude Code is asked to:

**"Improve the DSPy signature for fact extraction"**
- Claude can reference `llms.txt` for DSPy signature best practices
- Understand type-safe field definitions
- Learn about input/output constraints
- See examples of effective field descriptions

**"Add support for a new LLM provider"**
- Claude can reference adapter patterns in `llms.txt`
- Understand configuration approaches
- See integration examples
- Learn about provider-specific considerations

**"Refactor the FactExtractor class"**
- Claude can reference module design patterns
- Understand composition best practices
- Learn about ChainOfThought integration
- See how to structure complex LLM workflows

## Integration with Project

The `llms.txt` file is:
- **NOT** part of the application logic
- **NOT** executed as code
- **IS** a reference document for Claude Code understanding
- **IS** optional but helpful for DSPy-related development

## How to Invoke llms.txt References

When working with Claude Code, you can:

1. **Ask Claude to reference it**
   - "Based on llms.txt, how should I improve..."
   - "Per the DSPy patterns in llms.txt, suggest..."

2. **Let Claude proactively reference it**
   - Claude will automatically check `llms.txt` when working on DSPy components

3. **Point to specific sections**
   - "See the 'Signatures' section of llms.txt..."
   - "Reference the architecture patterns in llms.txt..."

## Benefits

- **Better Context**: Claude understands DSPy framework thoroughly
- **Informed Decisions**: Suggestions based on proven DSPy patterns
- **Consistency**: Aligns improvements with DSPy best practices
- **Efficiency**: Faster development with framework expertise
- **Quality**: Higher-quality code that leverages DSPy properly

## Related Files

- `CLAUDE.md` - Main development guide (points to this file)
- `esia_extractor.py` - Implementation using DSPy
- `skill-package/docs/` - Additional documentation

## Updates

As DSPy evolves or new patterns are discovered:
1. Update `llms.txt` with new information
2. Reference the latest in CLAUDE.md
3. Claude Code will automatically use the updated reference

---

**Key Takeaway**: Use `llms.txt` as a shared knowledge base between you and Claude Code for all DSPy-related development and enhancement of the ESIA Fact Extractor.
