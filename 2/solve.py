b = 10
def f(a):
    print(a)
    print(b)
    b = 15

f(3)

"""
Приведет к ошибке: UnboundLocalError: cannot access local variable 'b' where it is not associated with a value
Основная проблема здесь в том, что переменная b объявлена в глобальной области видимости, 
но внутри функции f пытается измениться без явного указания на глобальную область.
"""