"""
Application configuration
=========================
"""

from pathlib import Path

# Application root directory
APP_ROOT_DIR = Path(__file__).parent.parent

RESOURCES_DIR = APP_ROOT_DIR / "resources"

AUDIO_DIR = RESOURCES_DIR / "audio"

RECORDINGS_DIR = AUDIO_DIR / "recordings"

CHATS_AUDIO_DIR = AUDIO_DIR / "chats"


app_dirs = [RESOURCES_DIR, AUDIO_DIR, RECORDINGS_DIR, CHATS_AUDIO_DIR]
