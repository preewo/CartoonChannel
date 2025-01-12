from enum import Enum


# Enums for series response keys
class SeriesResponseKeys(Enum):
    NAME = 'name'
    OVERVIEW = 'overview'
    STATUS = 'status'
    FIRST_AIRED = 'firstAired'
    LAST_AIRED = 'lastAired'
    ORIGINAL_COUNTRY = 'originalCountry'
    ORIGINAL_LANGUAGE = 'originalLanguage'
    IMAGE = 'image'
    GENRES = 'genres'

# Enums for episode response keys
class EpisodeResponseKeys(Enum):
    SEASON_NUMBER = 'seasonNumber'
    EPISODE_NUMBER = 'number'
    TITLE = 'name'
    OVERVIEW = 'overview'
    AIRED = 'aired'
    IMAGE = 'image'