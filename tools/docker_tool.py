"""
Docker Tool for FrankenAgent — Phase 3 Graft
"""

import subprocess
import json
from typing import Optional


def docker_build(image_name: str, dockerfile_path: str = ".") -> str:
    """Build a Docker image from Dockerfile. Returns build output."""
    try:
        result = subprocess.run(
            ["docker", "build", "-t", image_name, dockerfile_path],
            capture_output=True, text=True, timeout=300
        )
        return f"Build stdout: {result.stdout}\nStderr: {result.stderr}\nReturn code: {result.returncode}"
    except Exception as e:
        return f"Error: {str(e)}"


def docker_run(container_name: str, image_name: str, ports: Optional[str] = None) -> str:
    """Run a container from image. Ports as '8000:8000'."""
    try:
        cmd = ["docker", "run", "-d", "--name", container_name]
        if ports:
            cmd += ["-p", ports]
        cmd += [image_name]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return f"Run output: {result.stdout}\nError: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


def docker_exec(container_name: str, command: str) -> str:
    """Execute command inside running container."""
    try:
        result = subprocess.run(
            ["docker", "exec", container_name] + command.split(),
            capture_output=True, text=True, timeout=60
        )
        return f"Exec output: {result.stdout}\nError: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


def docker_ps() -> str:
    """List running containers."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "json"],
            capture_output=True, text=True
        )
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


def docker_stop(container_name: str) -> str:
    """Stop a running container."""
    try:
        result = subprocess.run(
            ["docker", "stop", container_name],
            capture_output=True, text=True
        )
        return f"Stopped: {result.stdout}" if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


# Tool metadata for registry
TOOLS = {
    "docker_build": {
        "function": docker_build,
        "description": "Build Docker image from Dockerfile",
        "params": ["image_name", "dockerfile_path"]
    },
    "docker_run": {
        "function": docker_run,
        "description": "Run Docker container",
        "params": ["container_name", "image_name", "ports"]
    },
    "docker_exec": {
        "function": docker_exec,
        "description": "Execute command in container",
        "params": ["container_name", "command"]
    },
    "docker_ps": {
        "function": docker_ps,
        "description": "List running containers",
        "params": []
    },
    "docker_stop": {
        "function": docker_stop,
        "description": "Stop container",
        "params": ["container_name"]
    },
}
