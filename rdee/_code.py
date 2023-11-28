# coding=utf-8

#**********************************************************************
# this function is used to perform pretty and prescribed skeleton comments
#**********************************************************************
def norm_skComments(C, level = 1, language = 'ncl') : # normalize skeleton comments
    import sys

    if language == 'ncl' :
        cl = ';' # comment label
    elif language == 'python':
        cl = '#'
    else:
        print('unknwon language : {}'.format(language))
        sys.exit(1)

    if level == 1: # final 60
        charL = '>'
        charR = '<'
        lenCharL = ((59 - 4) - len(C)) // 2
        lenCharR = 59 - 4 - len(C) - lenCharL
        res = "{} {} {} {}".format(cl, charL * lenCharL, C, charR * lenCharR)
    elif level == 2:
        res = "{} {} {}".format(cl, '=' * 15, C)
    elif level == 3:
        res = "{} {} {}".format(cl, '~' * 10, C)
    elif level == 4:
        res = "{} {} {}".format(cl, '-' * 5, C)

    print(res)



#**********************************************************************
# this function is used to check if a function has a return value
#**********************************************************************
def has_return_value(func):
    import inspect
    import ast
    tree = ast.parse(inspect.getsource(func))
    return any(isinstance(node, ast.Return) for node in ast.walk(tree))



#**********************************************************************
# this function is used to check if a function has a return value
# Use dir(), pkgutil. may work as well
#**********************************************************************
def get_submodules(module, alias: str = None):
    import types
    
    assert isinstance(module, types.ModuleType)

    if not hasattr(get_submodules, 'obj_set'):
        outermost_flag = 1
        setattr(get_submodules, 'obj_set', set())

    get_submodules.obj_set.add(module.__name__)
    
    try:  #>- check fully initialized
        dir(module)
    except:
        return []
        
    # print(mod_str)
    # time.sleep(0.1)
    for img in dir(module):
        if img.startswith('_'):
            continue
        attr_str = f'module.{img}'
        try:
            attr = eval(attr_str)
        except:
            continue
        if isinstance(attr, types.ModuleType) and \
           attr.__name__ not in get_submodules.obj_set and \
           attr.__name__.startswith(module.__name__):
            # >- 1. check module; 2. ensure no circular; 3.avoid external module
            get_submodules(attr)
    
    # >>>>>>> remove the obj_set after the whole statistics
    if 'outermost_flag' in locals():
        rst = get_submodules.obj_set
        delattr(get_submodules, 'obj_set')
        if alias is not None:
            rst = {_.replace(module.__name__, alias, 1) for _ in rst}
        return list(rst)        



#**********************************************************************
# this function is used to get all submodules for target module
#**********************************************************************
def search_api(module, api: str, alias: str = None) -> list[str]:
    submodules = get_submodules(module, 'module')

    rst = []
    for sm in submodules:
        try:
            if hasattr(eval(sm), api):
                rst.append(f'{sm}.{api}')
        except:
            continue

    return [_.replace('module', module.__name__ if alias is None else alias) for _ in rst]