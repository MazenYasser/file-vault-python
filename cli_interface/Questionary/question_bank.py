from pathlib import Path

import questionary

from .question_routing import action_choices


def initialize_question_bank(cfg):
    """
    Dynamically builds the question bank

    Args:
        cfg (Config): The Config class, must be called to get the upload_destination

    Returns:
        dict: A dictionary represting a question_bank
    """
    file_choices = [str(file.name) for file in Path.iterdir(Path(cfg.upload_destination)) if file.is_file()]
    file_choices.append("Go Back ⬅")
    return {
        "choose_action" : questionary.select(
            message="Choose action:",
            choices=action_choices,
            use_indicator=True,
            use_shortcuts=True,
            show_selected=True,
            use_emacs_keys=True,
        ),
        "select_file_upload": questionary.path(message="Select file or enter file path"),
        "select_file_download": questionary.select(
            message="Select the file you want to download: ",
            choices=file_choices
        ),
    }