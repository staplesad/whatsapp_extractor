import re
import datetime as dt
from collections import defaultdict
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from . import util


class DataLoader:
    def __init__(self, config_loc=None):
        self.header_re = re.compile(
                "\d{2}\/\d{2}\/\d{4}, \d{2}\:\d{2} - ([\w|\(|\)]+(?: \w+)?):")
        self.ts_re = re.compile("\d{2}\/\d{2}\/\d{4}, \d{2}\:\d{2} -")
        self.cfg = util.Config(config_loc)
        self.senders = self.cfg.senders
        self.remove_media = self.cfg.remove_media or True
        self.remove_tags = self.cfg.remove_tags or True

    def load_line(self, line: str) -> Tuple[str, Optional[str], Optional[str], bool]:
        header_match = self.header_re.match(line)
        ts_match = self.ts_re.match(line)
        header = None
        sender = None
        from_sender = True
        header_end = 0
        if header_match:
            header = header_match.group()
            sender = header_match.group(1)
            header_end = header_match.end()+1
        elif ts_match:
            header = ts_match.group()
            header_end = ts_match.end()+1
            from_sender = False
        message = line[header_end:]
        return message, header, sender, from_sender

    @staticmethod
    def merge_broken_messages(messages: List[str],
                              senders: List[Optional[str]],
                              from_senders: List[bool]) -> Tuple[List[str], List[Optional[str]]]:
        merged_messages: List[str] = []
        indexes: List[int] = []
        for i, (message, sender, from_sender) in enumerate(
                zip(messages, senders, from_senders)):
            if from_sender and not sender:
                merged_messages[-1] += message
            else:
                merged_messages.append(message)
                indexes.append(i)
        return merged_messages, indexes

    def get_datetime(self, headers: List[str]) -> List[dt.datetime]:
        datestrings = [self.ts_re.match(h).group() for h in headers]
        datetime_format = "%d/%m/%Y, %H:%M -"
        return [dt.datetime.strptime(d, datetime_format) for d in datestrings]

    def load_file(self, filename: str) -> pd.DataFrame:
        output_dict = defaultdict(list)
        with open(filename) as fp:
            for line in fp:
                m, h, s, from_s = self.load_line(line)
                output_dict['messages'].append(m)
                output_dict['headers'].append(h)
                output_dict['senders'].append(s)
                output_dict['from_sender'].append(from_s)
        merged_messages, idx = self.merge_broken_messages(
                output_dict['messages'],
                output_dict['senders'], output_dict['from_sender'])
        output_dict['messages'] = merged_messages
        output_dict['senders'] = np.array(output_dict['senders'])[idx]
        output_dict['headers'] = np.array(output_dict['headers'])[idx]
        del output_dict['from_sender']
        output_dict['timestamp'] = self.get_datetime(output_dict['headers'])
        return pd.DataFrame(output_dict)

    def id_messy_message(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        pass
