from yaml import safe_load

class Config:
    def __init__(self, config_loc=None):
        self.bare_cfg = None
        self.senders = None
        self.remove_media = None
        self.remove_tags = None
        if not config_loc:
            print('No config file location given.')
        else:
            self.bare_cfg = safe_load(config_loc)
            self.senders = self.bare_cfg['senders']
            self.remove_media = self.bare_cfg['remove_media']
            self.remove_tags = self.bare_cfg['remove_tags']
