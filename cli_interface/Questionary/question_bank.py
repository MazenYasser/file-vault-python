import questionary
from .question_routing import action_choices

question_bank = {
    "choose_action" : questionary.select(
        message="Choose action:",
        choices=action_choices,
        use_indicator=True,
        use_shortcuts=True,
        show_selected=True,
        use_emacs_keys=True,
    ),
    "select_file_upload": questionary.path(message="Select file or enter file path"),
    "select_file_download": questionary.path(message="Select file or enter file path"),
}