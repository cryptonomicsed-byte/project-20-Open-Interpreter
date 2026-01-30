#!/usr/bin/env python3
"""
FrankenAgent Core — Minimal sovereign agent powered by Ollama

Usage:
    python agent_core.py "Build a FastAPI hello app, containerize it, run it"
"""

import requests
import json
import sys
from tools.docker_tool import TOOLS as DOCKER_TOOLS


OLLAMA_API_BASE = "http://localhost:11434"
OLLAMA_MODEL = "deepseek-coder:6.7b"


def call_ollama(prompt: str, tools_context: str = "") -> str:
    """Call Ollama API for reasoning."""
    full_prompt = f"""{tools_context}

User Request: {prompt}

Available Tools:
{json.dumps({k: v['description'] for k, v in DOCKER_TOOLS.items()}, indent=2)}

Think step-by-step. Respond with tool calls in the format:
TOOL: docker_build(image_name="hello", dockerfile_path=".")
OR natural reasoning if no tool is needed.
"""
    
    try:
        response = requests.post(
            f"{OLLAMA_API_BASE}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": full_prompt, "stream": False},
            timeout=120
        )
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Ollama error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "ERROR: Ollama not running. Start with: ollama serve"
    except Exception as e:
        return f"ERROR: {str(e)}"


def execute_tool(tool_name: str, **kwargs) -> str:
    """Execute a tool from registry."""
    if tool_name in DOCKER_TOOLS:
        tool_func = DOCKER_TOOLS[tool_name]["function"]
        return tool_func(**kwargs)
    return f"Tool '{tool_name}' not found."


def agent_loop(user_request: str):
    """Main agent loop: reason → plan → execute → feedback."""
    print(f"\n🔥 FrankenAgent activated with request:\n{user_request}\n")
    
    # Phase 1: Reason about request
    reasoning = call_ollama(user_request)
    print(f"🧠 Reasoning:\n{reasoning}\n")
    
    # Phase 2: Parse tool calls (simplified)
    if "docker_build" in reasoning:
        print("→ Executing docker_build...")
        result = execute_tool("docker_build", image_name="hello-api", dockerfile_path=".")
        print(f"Result: {result}\n")
    
    if "docker_run" in reasoning:
        print("→ Executing docker_run...")
        result = execute_tool("docker_run", container_name="hello-api", image_name="hello-api", ports="8000:8000")
        print(f"Result: {result}\n")
    
    if "docker_exec" in reasoning or "curl" in reasoning.lower():
        print("→ Testing with curl...")
        result = execute_tool("docker_exec", container_name="hello-api", command="sh -c curl localhost:8000")
        print(f"Result: {result}\n")
    
    print("✅ Agent cycle complete.\n")


if __name__ == "__main__":
    user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Build a FastAPI hello app, containerize it, run it on 8000:8000"
    agent_loop(user_input)
