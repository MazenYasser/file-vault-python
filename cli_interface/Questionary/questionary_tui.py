import sys

from app.settings import get_config

from .question_bank import initialize_question_bank
from .question_routing import routes


class QuestionaryTUI():
    def __init__(self, vault) -> None:
        self.vault = vault
    
    def run(self):
        cfg = get_config()
        question_bank = initialize_question_bank(cfg)
        chosen_action = question_bank["choose_action"].ask()
        # chosen_acion being None means the user made a KeyboardInterrupt, this is the way questionary handles KeyboardInterrupt
        if chosen_action is None:
            print("Bye!")
            sys.exit(0)
        action_choice = routes.get(chosen_action, None)
        if action_choice is None:
            raise NotImplementedError("This action has not been implemented yet.")
        action_choice(question_bank=question_bank, vault=self.vault)
