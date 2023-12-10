"""Models for the "gamecms_hacs" authority."""

import datetime as dt

from pydantic import Field, model_validator

from .base import CamelCaseModel, PascalCaseModel
from .refdata import MedalDifficulty, MedalType


class TranslatableString(CamelCaseModel):
    """A string value accompanied by a dictionary of translations.

    Attributes:
        value: The string value.
        translations: A dictionary of language codes to translations for the string value.
    """

    value: str
    translations: dict[str, str]


class Medal(CamelCaseModel):
    """Metadata for a single medal.

    Attributes:
        name_id: The medal's ID.
        name: The medal's name.
        description: The medal's description.
        sprite_index: The index of the medal's sprite in the sprite sheet.
        sorting_weight: The medal's sorting weight.
        difficulty: The medal's difficulty, such as "normal" or "legendary".
        type: The medal's type, such as "mode" or "proficiency".
        personal_score: The amount of personal score awarded by obtaining the medal.
    """

    name_id: int
    name: TranslatableString
    description: TranslatableString
    sprite_index: int
    sorting_weight: int
    difficulty: MedalDifficulty = Field(alias="difficultyIndex")
    type: MedalType = Field(alias="typeIndex")
    personal_score: int


class SpriteSheet(CamelCaseModel):
    """Information about a sprite sheet that contains medal sprites.

    Attributes:
        path: The path to the sprite sheet, relative to the "gamecms_hacs" host.
        columns: The number of columns in the sprite sheet.
        size: The size of each sprite in the sprite sheet.
    """

    path: str
    columns: int
    size: int


class SpriteSheets(CamelCaseModel):
    """Sizes of sprite sheets that contain medal sprites.

    Attributes:
        small: A sprite sheet with small sprites.
        medium: A sprite sheet with medium sprites.
        extra_large: A sprite sheet with extra large sprites.
    """

    small: SpriteSheet
    medium: SpriteSheet
    extra_large: SpriteSheet = Field(alias="extra-large")


class MedalMetadata(CamelCaseModel):
    """Metadata for all medals.

    Attributes:
        difficulties: The list of possible difficulties.
        types: The list of possible types.
        sprites: Information about the medal sprite sheets that contain medal.
        medals: The list of available medals.
    """

    difficulties: list[str]
    types: list[str]
    sprites: SpriteSheets
    medals: list[Medal]


class CsrSeason(PascalCaseModel):
    """A CSR season.

    Attributes:
        csr_season_file_path: The relative path to the CSR season file. The stem
            of the path is the CSR season's ID, e.g., "CsrSeason5-1".
        start_date: The UTC start date of the season.
        end_date: The UTC end date of the season.
    """

    csr_season_file_path: str
    start_date: dt.datetime
    end_date: dt.datetime

    @model_validator(mode="before")
    def _flatten_dates(cls, values):
        """Flatten the date objects."""
        for key in ("StartDate", "EndDate"):
            values[key] = values[key]["ISO8601Date"]
        return values


class CsrSeasonCalendar(PascalCaseModel):
    """A collection of past and current CSR seasons.

    Attributes:
        seasons: The list of CSR seasons.
    """

    seasons: list[CsrSeason]
