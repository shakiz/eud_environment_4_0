import random

import app_dir.main.application_manager as am
import re
import ast
import copy
import time

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
        for k, value in self.mapping_dict.items():
            required_val = value[1]
            print("value[1]:::"+str(value[1]))
            print("Context Values :: : : : :: : "+str(context_values))
            for cv in context_values:
                print("current context value + required_val "+cv+"|||||"+required_val)
                if cv in required_val:
                    print("Selected Variant : " + str(value[len(value)-1]))
                    selected_variant = value[len(value)-1]
                else:
                    print("No match")
            #if value[1][:-1] in context_values:
            #if any(substring in string for substring in context_values):

        return selected_variant


class RuntimeEngine:

    variant = ""

    def __init__(self) -> None:
        super.__init__()

    def get_and_set_code(self, variant):
        self.variant = variant
        return

    def execute_code(self):
        while True:
            time.sleep(2)
            code_ast = ast.parse(self.code)

            init_ast = copy.deepcopy(code_ast)
            init_ast.body = code_ast.body[:-1]

            last_ast = copy.deepcopy(code_ast)
            last_ast.body = code_ast.body[-1:]

            exec(compile(init_ast, "<ast>", "exec"), globals())
            if type(last_ast.body[0]) == ast.Expr:
                return eval(compile(convert_expr_expression(last_ast.body[0]), "<ast>", "eval"), globals())
            else:
                exec(compile(last_ast, "<ast>", "exec"), globals())

    def print_result(self):
        result = self.execute_code(self)
        print(result)


def convert_expr_expression(expr):
    expr.lineno = 0
    expr.col_offset = 0
    result = ast.Expression(expr.value, lineno=0, col_offset=0)

    return result














