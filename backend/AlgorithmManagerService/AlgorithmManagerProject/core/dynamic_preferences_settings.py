

class DynamicPreferencesGeneralSection:
    section_name = "general"

    def __init__(self, full_key=False):
        self.full_key = full_key

    @property
    def max_links_remote_download(self):
        name = "max_links_remote_download"
        if self.full_key:
            return f"{self.section_name}__{name}"
        return name


