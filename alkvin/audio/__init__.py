from .bus import AudioBus


def get_audio_bus():
    """Return the audio bus singleton."""
    if not hasattr(get_audio_bus, "audio_bus"):
        get_audio_bus.audio_bus = AudioBus()

    return get_audio_bus.audio_bus
