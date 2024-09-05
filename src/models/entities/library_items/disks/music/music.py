from pydantic import Field

from src.models.entities.library_items.disks.disks import Disk


class MusicCD(Disk):
    band: str = Field(..., max_length=100, description="Band or artist name")
    genre: str = Field(..., max_length=50, description="Genre of the music CD")

