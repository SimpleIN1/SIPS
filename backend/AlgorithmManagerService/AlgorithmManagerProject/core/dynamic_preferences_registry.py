
from dynamic_preferences.types import BooleanPreference, StringPreference, IntegerPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.users.registries import user_preferences_registry

from core.dynamic_preferences_settings import DynamicPreferencesGeneralSection

global_pref = global_preferences_registry.manager()
general = Section(DynamicPreferencesGeneralSection.section_name)


@global_preferences_registry.register
class MaxLinksRemoteDownload(IntegerPreference):
    section = general
    name = DynamicPreferencesGeneralSection().max_links_remote_download
    default = '50'
    required = True
