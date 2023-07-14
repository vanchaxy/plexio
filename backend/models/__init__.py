from backend.models.plex import PlexMediaType
from backend.models.stremio import StremioMediaType

PLEX_TO_STREMIO_MEDIA_TYPE = {
    PlexMediaType.show: StremioMediaType.series,
    PlexMediaType.movie: StremioMediaType.movie,
}

STREMIO_TO_PLEX_MEDIA_TYPE = {v: k for k, v in PLEX_TO_STREMIO_MEDIA_TYPE.items()}
