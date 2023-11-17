'''
格式化算式模块
功能：将算式格式化为列表
'''
import re
from decimal import Decimal, getcontext

def Pretty(formula,mode):
    formula_list = []
    err=0
    if mode == 1:
        formula = re.sub(' ', '', formula)  # 去掉算式中的空格s
        # 以 '横杠数字' 分割， 其中正则表达式：(\-\d+\.?\d*) 括号内：
        # \- 表示匹配横杠开头；\d+ 表示匹配数字1次或多次；\.?表示匹配小数点0次或1次;\d*表示匹配数字0次或多次。
        formula_list = [i for i in re.split('(-[\d+,π,e]\.?\d*)', formula) if i]
        formula_list[0] = (formula_list[0][0] == '(') * "1*" + (formula_list[0][0] == "-") * "0" + formula_list[0]
        final_formula = []  # 最终的算式列表
        for item in formula_list:
            # 算式以横杠开头，则第一个数字为负数，横杠为负号
            if len(final_formula) == 0 and re.match('-[\d+,π,e]\.?\d*$', item):
                final_formula.append(item)
                continue
            # 如果当前的算式列表最后一个元素是运算符['+', '-', '*', '/', '('， '%'， '^'], 则横杠为减号
            if len(final_formula) > 0:
                if re.match('[\+\-\*\/\(\%\^]$', final_formula[-1]):
                    final_formula.append(item)
                    continue
            # 按照运算符分割开
            item_split = [i for i in re.split('([\+\-\*\/\(\)\%\^\√])', item) if i]
            final_formula += item_split
    elif mode == 2:
        getcontext().prec = max(len(formula[0]), len(formula[1]), len(formula[2]),len(formula[3]),len(formula[4]))
        if (Decimal(formula[0])>=Decimal(formula[4])
                or Decimal(formula[1])>=Decimal(formula[4])
                or Decimal(formula[2])>=Decimal(formula[4])
                or Decimal(formula[3])>=Decimal(formula[4])):
            err="系数大于Base，请重新输入"
            return formula_list,err
        else:
            final_formula = formula
    elif mode == 3:
        getcontext().prec = max(len(formula[0]), len(formula[1]), len(formula[2]))*2
        if Decimal(formula[0])>=Decimal(formula[2])**2 or Decimal(formula[1])>=Decimal(formula[2])**2:
            err="大数大于Base^2，请重新输入"
            return formula_list,err
        else:
            final_formula = [str(Decimal(formula[0])//Decimal(formula[2])),
                             str(Decimal(formula[0])%Decimal(formula[2])),
                             str(Decimal(formula[1]) // Decimal(formula[2])),
                             str(Decimal(formula[1]) % Decimal(formula[2])),
                             formula[2],
                             formula[3]]
    # print("格式化算式：", final_formula)
    return final_formula,err