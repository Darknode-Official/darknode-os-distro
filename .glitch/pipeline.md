# Project Pipeline Guide

<!-- iCode reads this file as an MCP resource. Keep it up to date. -->

## Project Overview

[Brief description of what this project does and its technology stack]

## Development Workflow

This project uses iCode pipelines for structured AI-assisted development.

### Available Pipelines

| Pipeline | Description | When to Use |
|----------|-------------|-------------|
| [pipeline-name] | [description] | [when] |

### Standard Feature Pipeline

For implementing a new feature, use:
```
glitch pipeline run feature-pipeline --var feature_name="..."
```

Or ask your AI agent: "Run the feature pipeline for [feature description]"

## Project Conventions

- Language/framework: [e.g., TypeScript, Node.js]
- Test framework: [e.g., Vitest]
- Build command: [e.g., pnpm build]
- Test command: [e.g., pnpm test]
- Code style: [e.g., ESLint + Prettier]

## Pipeline Variables

Common variables used across pipelines:
- `feature_name`: Short name for the feature being built
- `artifacts_dir`: Output directory (default: docs/)

## Notes for AI Agents

When working on this project:
1. Check this file for the right pipeline to use
2. Use `list_pipelines` MCP tool to see available pipelines
3. Start with `run_pipeline` for complex features
4. Monitor progress with `get_run_status`
