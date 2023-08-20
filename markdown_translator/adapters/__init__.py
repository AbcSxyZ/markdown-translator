from .adapters_manager import AdaptersManager
from .hashes_adapters import *
from .translators import *
from ..configuration import config

hashes_adapters_collection = {
    "json": BlockHashesJSONAdapter,
    "sql": BlockHashesSQLAdapter,
    "disabled": BlockHashesAdapter,
    }

translator_adapters_collection = {
    "deepl": translate_deepl,
    "disabled": translate_disabled,
}

hashes = AdaptersManager(
    adapters=hashes_adapters_collection,
    config_var="VERSIONING"
    )

translator = AdaptersManager(
    adapters=translator_adapters_collection,
    config_var="TRANSLATION_ENGINE"
    )
