"""
Portfolio Package Initialization

This package contains the core logic for:
- Enhancing portfolio content with Gemini AI
- Rendering HTML portfolio with Jinja2
"""

from .generator import generate_portfolio
from .enhancer import enhance_content

__all__ = ["generate_portfolio", "enhance_content"]
