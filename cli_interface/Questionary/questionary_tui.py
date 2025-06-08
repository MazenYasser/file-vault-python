import sys
from .question_bank import question_bank
from .question_routing import routes

class QuestionaryTUI():
    def __init__(self, vault) -> None:
        self.vault = vault
    
    def run(self):
        chosen_action = question_bank["choose_action"].ask()
        if chosen_action is None:
            print("Bye!")
            sys.exit(0)
        action_choice = routes.get(chosen_action)
        if action_choice not in routes:
            raise NotImplementedError("This action has not been implemented yet.")
        action_choice(question_bank=question_bank, vault=self.vault)
        
