from app.vault_app import FileVaultApp
from app.config import *
from .question_bank import question_bank
from .question_routing import routes

class QuestionaryTUI():
    def __init__(self, vault: FileVaultApp) -> None:
        self.vault = vault
    
    def run(self):
        chosen_action = question_bank["choose_action"].ask()
        routes[chosen_action](question_bank, self.vault)
