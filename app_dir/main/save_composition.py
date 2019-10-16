from __future__ import print_function
from app_dir.main.forms import *
import ast
import copy


def convertExpr2Expression(Expr):
    Expr.lineno = 0
    Expr.col_offset = 0
    result = ast.Expression(Expr.value, lineno=0, col_offset=0)

    return result


def exec_with_return(code):
    code_ast = ast.parse(code)

    init_ast = copy.deepcopy(code_ast)
    init_ast.body = code_ast.body[:-1]

    last_ast = copy.deepcopy(code_ast)
    last_ast.body = code_ast.body[-1:]

    exec(compile(init_ast, "<ast>", "exec"), globals())
    if type(last_ast.body[0]) == ast.Expr:
        return eval(compile(convertExpr2Expression(last_ast.body[0]), "<ast>", "eval"), globals())
    else:
        exec(compile(last_ast, "<ast>", "exec"), globals())


def save_com(request):
    if request.is_ajax():
        code = request.POST['code']
        result = exec_with_return(code)
        print(code)
        print(result)
    else:
        return HttpResponse('Use ajax format!')

    return JsonResponse({'code': result})


