import random
from app_dir.main.generated_functions import *
import app_dir.main.application_manager as am
import re
import ast
import copy
import time
import json
import requests

regex_mapper = re.compile(r"(if).*?:$", re.MULTILINE)
variant = {}
context_values = []


def get_context():
    cm = am.ContextManager()
    #request_variant()
    while True:
        time.sleep(2)
        context_values.append(cm.watch_context())
        AdaptationEngine.get_selected_variant(AdaptationEngine)
        print("IN AE As CM ::::: "+str(cm.watch_context()))
    return


def request_variant():
    vm = am.VariantManager()

    print("request_variant() called")
    print(am.variants)
    print("----Acquired variants----")
    for key, value in variant.items():
        print(key, 'corresponds to', value)
    return


class AdaptationEngine:
    app_id = ""
    code = ""
    mapping_dict = {}

    def __init__(self) -> None:
        super.__init__()

    def set_variants(self, variants):
        variant = variants
        print("test ===== "+str(variant))

    def set_details(self, app_id, code):
        self.app_id = app_id
        self.code = code
        print("-----------------Adaptation Engine-------------")
        self.mapper(self)
        get_context()
        #RuntimeEngine.get_and_set_code(RuntimeEngine, self.get_selected_variant(self))
        print("-----------------Adaptation Engine-------------")
        return

    def mapper(self):
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
                    if regex_mapper.match(item_code):
                        print("Matched code  :::>>>:::: "+item_code)
                        context_with_required_value_cs = item_code.split("==")
                        print("Context :::: "+str(context_with_required_value_cs))
                        cs_ = code_list[i+1].strip()
                        print("Conditional service _cs :::: "+cs_)
                        context_with_required_value_cs.insert(len(context_with_required_value_cs), cs_)
                        print("context_with_required_value_cs :: "+str(context_with_required_value_cs))
                        self.mapping_dict["mapped_value"+str(i)] = context_with_required_value_cs
        for k, v in self.mapping_dict.items():
            print(k, ':::::corresponds to::::', v)
        return

    def get_selected_variant(self):
        #while True:
            #time.sleep(1)
            #print("time:::::"+get_am_pm())
        for k, value in self.mapping_dict.items():
            rm = RuntimeEngine()
            required_val = value[1]
            print("value[1]:::"+str(value[1]))
            print("Context Values :: : : : :: : "+str(context_values))
            for cv in context_values:
                print("current context value + required_val "+cv+"|||||"+required_val)
                if cv in required_val:
                    print("Selected Variant : " + str(value[len(value)-1]))
                    selected_variant = value[len(value)-1]
                    print(str(selected_variant))
                    rm.get_and_set_code(selected_variant)
                else:
                    vm = am.VariantManager()
                    services = vm.services
                    selected_variant = services[random.randint(0, 1)]
                    print(str(selected_variant))
                    rm.get_and_set_code(selected_variant)
                    #exec(selected_variant)
                    #print(str((newspaper_headlines('bitcoin', '2019-11-12', 'publishedAt'))))
            #if value[1][:-1] in context_values:
            #if any(substring in string for substring in context_values):

        return selected_variant


class RuntimeEngine:

    def __init__(self):
        print("in init runtime engine")

    def get_and_set_code(self, variant):
        self.exec_print_result(variant)
        return

    def exec_print_result(self,variant):
        result = exec(variant)
        print("From Runtime Engine"+str(result))
















