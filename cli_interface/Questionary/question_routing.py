from enum import Enum
from .sequence_functions import trigger_download_sequence, trigger_upload_sequence, trigger_exit_sequence

class ActionChoices(Enum):
    UPLOAD = "Upload"
    DOWNLOAD = "Download"
    VIEW_CURRENT_FILES = "View current files"
    SHOW_ACTION_HISTORY = "Show action history"
    SETTINGS = "Settings"
    EXIT = "Exit"

action_choices = [choice.value for choice in ActionChoices]

routes = {
    ActionChoices.UPLOAD.value: trigger_upload_sequence,
    ActionChoices.DOWNLOAD.value: trigger_download_sequence,
    ActionChoices.EXIT.value: trigger_exit_sequence,
}


