
from tool_get_time import get_current_time
from tool_shell import shell_tool
from tool_requests import requests_toolkit
from tool_repl import python_tool
from tool_catholic_liturgy import get_liturgy_for_year_and_month_tool, get_liturgy_explanation_tool

# Add all tools to the tools list
tools = [shell_tool, python_tool, get_liturgy_for_year_and_month_tool, get_liturgy_explanation_tool]
# Extend the tools list with the toolkit's tools
tools.extend(requests_toolkit.get_tools())
