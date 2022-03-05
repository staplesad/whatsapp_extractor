from yaml import safe_load

class Config:
    def __init__(self, config_loc=None):
        self.bare_cfg = None
        self.senders = None
        self.replace_tags = None
        self.remove_media = None
        self.remove_tags = None
        if not config_loc:
            print('No config file location given.')
        else:
            print(f'Loading config from {config_loc}')
            with open(config_loc) as fp:
                self.bare_cfg = safe_load(fp)
            self.senders = self.bare_cfg['senders']
            if self.senders:
                self.senders = {str(k): v for k, v in self.senders.items()}
            self.replace_tags = self.bare_cfg['replace_tags']
            if self.replace_tags:
                self.replace_tags = {str(k): v for k, v in self.replace_tags.items()}
            self.remove_media = self.bare_cfg['remove_media']
            self.remove_tags = self.bare_cfg['remove_tags']
