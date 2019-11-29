import random
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
        VariantManager.register(VariantManager, app_id, code)


class ContextManager:
    code = ""
    app_id = ""
    services = []

    def __init__(self) -> None:
        super().__init__()

    def register(self, app_id, code):
        self.code = code
        self.app_id = app_id
        print("Context registered with application id :> " + app_id)
        return

    def get_context(self, app_id):
        self.watch_context(ContextManager)
        return

    def watch_context(self):
        self.services = VariantManager.get_services(VariantManager)
        print(self.services)
        # while True:
        # time.sleep(2)
        # weather = weather_info("Dhaka")
        # print(weather)
        return


class VariantManager:
    total_variant = ""
    code = ""
    app_id = ""
    services = []
    default_service_list = ['news', 'cricket', 'newspaper_headlines', 'doctor', 'recipe_puppy', 'print_content', 'value_to_print', 'print']

    regex_if_true = re.compile(r"^if\strue:|^if\sTrue:$", re.MULTILINE)
    regex_if_false = re.compile(r"^if\sfalse|^if\sFalse:$", re.MULTILINE)
    regex_service = re.compile(r"(if).*?:$", re.MULTILINE)
    regex_step_only = re.compile(r".*?", re.MULTILINE)

    def __init__(self) -> None:
        super().__init__()

    def register(self, app_id, code):
        self.code = code
        self.app_id = app_id
        print("Variant Registered with application id :> "+app_id)
        self.calculate_variant(self)
        return

    def calculate_variant(self):
        #Number of lines
        new_lines = len(self.code.split('\n'))
        print("New lines ===>> "+str(new_lines))

        #Split string into segments based on new line
        code_list = self.code.splitlines()
        for item in code_list:
            print("Item :> "+item+" Space count ==>> "+str(item.count(' ')))

        if len(code_list) > 1:
            print("More than 1 line")
            for item_code in code_list:
                if item_code.strip().startswith('if'):
                    if self.regex_if_true.match(item_code.strip()):
                        match_str = self.regex_if_true.match(item_code.strip())
                        print('matched_str[if_true]::' + match_str.group()[2:-1])
                        service = match_str.group()[2:-1]
                        self.services.append(service)
                        print('separated_service=>>>' + service)
                    elif self.regex_if_false.match(item_code.strip()):
                        match_str = self.regex_if_false.match(item_code.strip())
                        print('matched_str[if_false]::' + match_str.group()[2:-1])
                        service = match_str.group()[2:-1]
                        print('separated_service=>>>' + service)
                    elif self.regex_service.match(item_code.strip()):
                        match_str = self.regex_service.match(item_code.strip())
                        print('matched_str[service]::' + match_str.group()[2:-1])
                        service = match_str.group()[2:-1]
                        self.services.append(service)
                        print('separated_service=>>>' + service)
                    elif self.regex_step_only.match(item_code.strip()):
                        match_str = self.regex_step_only.match(item_code.strip())
                        print('matched_str[step_only]::' + match_str.group())
                        service = match_str.group()[2:-1]
                        self.services.append(service)
                        print('separated_service=>>>' + service)
                    else:
                        print("Does not match")
                elif any(item_code in string for string in self.default_service_list):
                    print('Default Item List Service Found =>>> '+item_code)
                else:
                    print("No match found.")
        elif len(code_list) == 1:
            print("Only One Statement")

        return

    def get_services(self):
        return self.services


def generate_id():
    app_id = app_name + "" + str(random.randint(1, 100))
    print('application_id::'+app_id)
    return app_id
