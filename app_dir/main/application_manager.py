from app_dir.main.generated_functions import *
import random
import time
import re

app_name = "eud_environment_"


class ApplicationManager:
    code = ""
    app_id = ""

    def __init__(self) -> None:
        super().__init__()

    def get_app(self, code):
        code = code
        print(code)
        app_id = generate_id()
        ContextManager.register(ContextManager, app_id, code)
        ContextManager.get_context(ContextManager, app_id)
        #VariantManager.register(VariantManager, app_id, code)


class ContextManager:
    code = ""
    app_id = ""
    service = ""
    # regex_if_true_false = re.compile(r'if\s+[\w-]+')
    regex_if_true = re.compile(r"^if\strue:|^if\sTrue:$", re.MULTILINE)
    regex_if_false = re.compile(r"^if\sfalse|^if\sFalse:$", re.MULTILINE)
    regex_service = re.compile(r"(if).*?:$", re.MULTILINE)

    def __init__(self) -> None:
        super().__init__()

    def register(self, app_id, code):
        print("registered_context")
        code = code

        if self.regex_if_true.match(code):
            match_str = self.regex_if_true.match(code)
            print('matched_str[if_true]::' + match_str.group()[2:-1])
            self.service = match_str.group()[2:-1]
            print('separated_service=>>>'+self.service)
        elif self.regex_if_false.match(code):
            match_str = self.regex_if_false.match(code)
            print('matched_str[if_false]::' + match_str.group()[2:-1])
            self.service = match_str.group()[2:-1]
            print('separated_service=>>>' + self.service)
        elif self.regex_service.match(code):
            match_str = self.regex_service.match(code)
            print('matched_str[service]::' + match_str.group()[2:-1])
            self.service = match_str.group()[2:-1]
            print('separated_service=>>>' + self.service)
        else:
            print("Does not match")
        #print("passed code to register context : " + code)
        return

    def get_context(self, app_id):
        self.watch_context(ContextManager)
        return

    def watch_context(self):
        # while True:
        # time.sleep(2)
        # weather = weather_info("Dhaka")
        # print(weather)
        return


class VariantManager:
    total_variant = ""
    code = ""

    def __init__(self) -> None:
        super().__init__()

    def register(self, app_id, code):
        code = code
        print("registered_variant")
        print("variant code:" + code)
        return

    def calculate_variant(self):
        return


def generate_id():
    app_id = app_name + "" + str(random.randint(1, 100))
    print('application_id::'+app_id)
    return app_id
