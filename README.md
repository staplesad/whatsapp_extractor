# Code for formatting WhatsApp exported messages into pandas DataFrame
- parses and merges messages; extracts senders and timestamps from .txt format exported messages
- messages where a sender is None correspond to notifications (such as Group created by __ or __ has changed their phone number).

## Assumptions about contact names
- They only contain Unicode word characters and characters (, ) and +. If a contact's name contains anything else it won't be parsed correctly
- It assumes that names do not contain more than 3 spaces.
- If you want to specify a mapping from e.g. phone numbers or nicknames to other names that can be defined in an optional config file.

## Config flags
See sample_config.yml for an example

- If the messages are exported without media any media sent shows up as "\<Media Omitted\>". These messages are removed if the `remove_media` flag is True. (default is True)
- If a message contains an @tagging of a contact this is shown in text as their phone number. These tags are removed if the `remove_tags` flag is True. (default is True)
- If you want to replace @tagged numbers with a specific string you can define a mapping in the config under `replace_tags`.
