# Continuous Context Session Compactor Skill for Autonomous Agents

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue.svg)](https://modelcontextprotocol.io)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](requirements.txt)

Enables long-horizon autonomous agents to run persistently without context window exhaustion. Automatically calculates token consumption and creates concise sliding summaries for elder turns.

## Capabilities
- **Token Budget Guarding**: Enforces strict configurable budget limits (e.g. 8k, 32k, 128k).
- **Sliding History Distillation**: Preserves critical system instructions and recent conversation while compressing historical turns.
- **Zero Overhead**: In-memory token estimation and distillation with zero external LLM dependencies.

## MCP Server Integration
```bash
python mcp_server.py
```

### Available MCP Tools
- `compact_messages`: Compact conversation array when exceeding token limits.
