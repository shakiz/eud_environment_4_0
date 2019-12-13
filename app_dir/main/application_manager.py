import time
from app_dir.main.adaptation_engine import *
import random
import re
import app_dir.main.generated_functions as gf

app_name = "eud_environment_"
variants = {}
regex_if_true = re.compile(r"^if\strue:|^if\sTrue:$", re.MULTILINE)
regex_if_false = re.compile(r"^if\sfalse|^if\sFalse:$", re.MULTILINE)
regex_service = re.compile(r"(if).*?:$", re.MULTILINE)
regex_step_only = re.compile(r".*?", re.MULTILINE)
city_regex = "(.)(weather_info)(.)(\\'.*?\\').*?(=)(=).*?(\\'.*?\\')"


class ApplicationManager:
    code = ""
    app_id = ""

    def __init__(self):
        print("in init")

    def get_app(self, code):
        code = code
        print(code)
        app_id = generate_id()
        ContextManager.register(ContextManager, app_id, code)
        VariantManager.register(VariantManager, app_id, code)
        AdaptationEngine.set_details(AdaptationEngine, app_id, code)


class ContextManager:
    code = ""
    app_id = ""
    context_list = []

    def __init__(self):
        print("in init context manager")

    def register(self, app_id, code):
        self.code = code
        self.app_id = app_id
        print("-------------------Context Manager------------------")
        print("Context registered with application id :> " + app_id)
        self.find_context(self)
        print("-------------------Context Manager------------------")
        return

    def unregister(self):
        self.code = ""
        self.app_id = ""
        self.context_list = []
        print("Unregistered >> Context Manager")

    def find_context(self):
        new_lines = len(self.code.split('\n'))
        print("New lines ===>> " + str(new_lines))

        # Split string into segments based on new line
        code_list = self.code.splitlines()
        for item in code_list:
            print("Item :> " + item + " Space count ==>> " + str(item.count(' ')))
        if len(code_list) > 1:
            for i in range(len(code_list)):
                item_code = code_list[i].strip()
                if item_code.startswith('if'):
                    if regex_if_true.match(item_code):
                        match_str = regex_if_true.match(item_code.strip())
                        print('matched_str[if_true]::' + match_str.group()[2:-1])
                        context = match_str.group()[2:-1]
                        self.context_list.append(context)
                        print('separated_service=>>>' + context)
                    elif regex_if_false.match(item_code):
                        match_str = regex_if_false.match(item_code.strip())
                        print('matched_str[if_false]::' + match_str.group()[2:-1])
                        context = match_str.group()[2:-1]
                        self.context_list.append(context)
                        print('separated_service=>>>' + context)
                    elif regex_service.match(item_code):
                        match_str = regex_service.match(item_code.strip())
                        print('matched_str[service]::' + match_str.group()[2:-1])
                        context = match_str.group()[2:-1]
                        self.context_list.append(context)
                        print('separated_service=>>>' + context)
                    elif regex_step_only.match(item_code):
                        match_str = regex_step_only.match(item_code.strip())
                        print('matched_str[step_only]::' + match_str.group())
                        context = match_str.group()[2:-1]
                        self.context_list.append(context)
                        print('separated_service=>>>' + context)
                    else:
                        print("Does not match")
                else:
                    print("No match found.")
        elif len(code_list) == 1:
            print("Only One Statement")
        return

    def watch_context(self):
        for context in self.context_list:
            print("Watching ::::: "+context)

            if 'weather' in context:
                rg = re.compile(city_regex, re.IGNORECASE | re.DOTALL)
                print(str(city_regex))
                m = rg.search(context)
                if m:
                    city = m.group(4)[1:-1]
                print("City : "+city)
                result = gf.weather_info(city)
            elif 'get_am_pm':
                result = get_am_pm()
            context_values.insert(0, result)
        print("Current Context :: " + result)
        return result


class VariantManager:
    code = ""
    app_id = ""
    conditional_services = []
    services = ["print_content('variant changes')", "(newspaper_headlines('bitcoin', '2019-11-13', 'publishedAt'))"]

    def __init__(self):
        print("in init variant manager")

    def register(self, app_id, code):
        self.code = code
        self.app_id = app_id
        print("-------------------Variant Manager------------------")
        print("Variant Registered with application id :> "+app_id)
        self.extract_variant(self)
        self.make_variant(self)
        print("-------------------Variant Manager------------------")
        return

    def unregister(self):
        self.app_id = ""
        self.code = ""
        self.services = []
        self.conditional_services = []
        self.variants = {}
        print("Unregistered >> Variant Manager")

    def extract_variant(self):
        # Split string into segments based on new line
        code_list = self.code.splitlines()
        for item in code_list:
            print("Item :> " + item + " Space count ==>> " + str(item.count(' ')))
        if len(code_list) > 1:
            for i in range(len(code_list)):
                if code_list[i].strip().startswith('if'):
                    item_code = code_list[i+1].strip()
                    print('matched_str[step_only]::' + item_code)
                    conditional = item_code
                    self.conditional_services.append(conditional)
                    print('separated_service=>>>' + conditional)
                else:
                    print("No match found.")
        elif len(code_list) == 1:
            print("Only One Statement")
        return

    def make_variant(self):
        length_cs = len(self.conditional_services)
        print("Length of CS :::: "+str(length_cs))

        for index in range(length_cs - 1, -1, -1):
            print(""+self.conditional_services[index])
            if length_cs==1:
                list_of_1_0 = list(map(int, str(format(1, '01b'))))
            else:
                list_of_1_0 = list(map(int, str(format(index, '02b'))))
            print(str(list_of_1_0))
            if all(value == 0 for value in list_of_1_0):
                print("All Values Are Zero,,So No CS")
                list_of_cs_and_s = self.services.copy()
                variants['variant' + str(index)] = list_of_cs_and_s
            elif all(value == 1 for value in list_of_1_0):
                print("ALl Values are One,, So ALl CS")
                list_of_cs_and_s = self.services.copy()
                for item in self.conditional_services:
                    list_of_cs_and_s.insert(len(list_of_cs_and_s), item)
                variants['variant' + str(index)] = list_of_cs_and_s
            else:
                list_of_cs_and_s = self.services.copy()
                for value in list_of_1_0:
                    if value == 1:
                        index_ = list_of_1_0.index(value)
                        cs_ = self.conditional_services[index_]
                        list_of_cs_and_s.insert(len(list_of_cs_and_s), cs_)
                        variants['variant' + str(index)] = list_of_cs_and_s

        self.get_variant(self)
        return

    def get_variant(self):
        for key, value in variants.items():
            print(key, 'corresponds to', value)
            variant[key] = value
        AdaptationEngine.set_variants(self, variants)
        return variants


def generate_id():
    app_id = app_name + "" + str(random.randint(1, 100))
    print('application_id::'+app_id)
    return app_id


def decimal_to_binary(num):
    if num > 1:
        decimal_to_binary(num // 2)
    return num % 2