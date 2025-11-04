"""
Dual Recommendation Health Assistant - AI Assistant Module
Provides health recommendations combining herbal remedies and pharmaceutical options.
"""

from .ai_assistant import (
    load_knowledge_base,
    generate_comprehensive_answer,
    format_answer_for_display,
    detect_condition_v2,
    generate_ai_insights
)

__all__ = [
    'load_knowledge_base',
    'generate_comprehensive_answer',
    'format_answer_for_display',
    'detect_condition_v2',
    'generate_ai_insights'
]

__version__ = "2.0.0"
__author__ = "Health Bridge AI"
