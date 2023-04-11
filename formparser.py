from form import Form
from bs4 import BeautifulSoup


class FormParser(list):

    def __init__(self, html: str):
        super().__init__()
        self._forms = []
        soup = BeautifulSoup(html, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            self.append(Form(form))

    def __str__(self):
        return f"Forms({len(self)}): {[str(form) for form in self]}"
