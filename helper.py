import time
from typing import List
from langchain_core.tools import Tool

def stream_data(input_string: str):
    """A generator that yields one character at a time from the input string."""
    for char in input_string.split(" "):
        yield char + " "
        time.sleep(0.02)

def find_tool_by_name(tools: List[Tool], name: str) -> Tool:
    """Find a tool by its name from a list of tools."""
    for tool in tools:
        if tool.name == name:
            return tool
    return None