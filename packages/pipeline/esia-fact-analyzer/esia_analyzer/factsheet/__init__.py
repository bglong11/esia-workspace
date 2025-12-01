"""
Factsheet generation modules for ESIA summary creation.

Implements a hybrid approach:
1. Static selection and organization of facts by domain
2. LLM-based surface realization for prose generation
3. Fallback to static templates when LLM is unavailable
4. Page-by-page fact distillation for Document Factsheet
"""

from .selector import FactSelector, DOMAIN_BUCKETS
from .generator import FactsheetGenerator
from .templates import generate_static_summary
from .page_distiller import PageDistiller

__all__ = [
    "FactSelector",
    "FactsheetGenerator",
    "DOMAIN_BUCKETS",
    "generate_static_summary",
    "PageDistiller"
]
