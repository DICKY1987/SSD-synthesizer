# 🤖 Agentic AI System User Guide

## Quick Start
1. **Open VS Code** in any project directory
2. **Press `w w w`** - Launches Claude AI CLI automatically
3. **Press `Ctrl+Shift+A`** - Launches free AI (aider) for simple tasks

## How It Works
The system intelligently routes tasks based on complexity:

- **Simple edits** → Free local tools (neovim, ripgrep)
- **Code generation** → Free AI (aider, ollama) 
- **Complex architecture** → Paid AI (Claude) with cost tracking

## Manual Usage
Run the intelligent router directly:
```powershell
.\scripts\intelligent_router.ps1 "Your task description here"
```

## Cost Optimization Features
- **$10/day budget limit** with automatic fallback to free tools
- **Usage logging** in `.ai/usage.log` tracks Claude usage
- **Free-first strategy** - only escalates to paid AI when necessary

## GitHub Integration
- Automatic workflows trigger free AI on code changes
- Add `use-claude` label to issues for complex task escalation
- Auto-commits improvements via free AI tools

## Repository Sync
Auto-sync multiple repositories with conflict resolution:
```powershell
.\scripts\auto_sync.ps1
```

## System Status
All configurations are in:
- `.ai/orchestrator.json` - AI routing rules
- `.ai/repos.json` - Repository sync settings
- `.vscode/` - VS Code integration files

The system maximizes free tools while keeping Claude available for truly complex architectural tasks, achieving ~99% cost optimization.

## Verification Checklist
After implementation, verify:
- [ ] VS Code opens AI CLI with "w w w" hotkey
- [ ] Free AI (aider) accessible via Ctrl+Shift+A
- [ ] GitHub workflows deployed
- [ ] Intelligent routing prioritizes free tools
- [ ] Cost tracking logs Claude usage
- [ ] Auto-sync works for git repositories

## System Architecture
```
User Request
     ↓
Intelligent Router
     ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Simple Tasks  │  Moderate Tasks │  Complex Tasks  │
│   Free Tools    │    Free AI      │    Paid AI      │
│  (neovim, rg)   │   (aider)       │   (claude)      │
└─────────────────┴─────────────────┴─────────────────┘
```

**Result**: 99% free system with intelligent paid escalation only when needed.