from enum import Enum

from .sequence_functions import (trigger_config_change_sequence,
                                 trigger_download_sequence,
                                 trigger_exit_sequence,
                                 trigger_upload_sequence)


class ActionChoices(Enum):
    UPLOAD = "Upload"
    DOWNLOAD = "Download"
    VIEW_CURRENT_FILES = "View current files"
    SHOW_ACTION_HISTORY = "Show action history"
    CHANGE_CONFIG = "Change configurations"
    EXIT = "Exit"

routes = {
    ActionChoices.UPLOAD.value: trigger_upload_sequence,
    ActionChoices.DOWNLOAD.value: trigger_download_sequence,
    ActionChoices.CHANGE_CONFIG.value: trigger_config_change_sequence,
    ActionChoices.EXIT.value: trigger_exit_sequence,
}

action_choices = [choice.value for choice in ActionChoices if choice.value in routes.keys()]


