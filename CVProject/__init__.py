# noqa: N999
"""CVProject package initialization."""

from .celery import app as celery_app

__all__ = ("celery_app",)
