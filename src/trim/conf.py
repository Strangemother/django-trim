"""Tools to assist with dynamic loadout of settings within trim and the
client site.
"""


class LiveConfigure(object):

    def installed_apps(self):
        """Return a list of strings to add to the INSTALLED_APPS"""
        return []

    def middleware(self):
        return []

    def configure_settings(self, name):
        print("configure_settings", name)
