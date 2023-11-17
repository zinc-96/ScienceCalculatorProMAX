from PrettyFormula import Pretty
from Calculate import Calculate
from ViewResult import ViewResult

if __name__ == '__main__':
    while(1):
        print("**********************************\n欢迎使用ScienceCalculatorProMAX")
        precision = 100
        mode = int(input("请选择模式\n1为普通计算\n2为大数以A1,B1,A2,B2,Base,operation格式输入\n3为大数以大数1,大数2,Base,operation格式输入\n模式："))
        if mode == 1:
            formula = input("请输入算式：")
            precision = int(input("请输入结果精度（默认100位）："))
        elif mode == 2:
            formula = input("请输入A1,B1,A2,B2,Base,operation：").split(',')
            if len(formula)!=6 or formula[5] not in ['+','-','*']:
                print("输入有误，程序结束")
                break
        elif mode == 3:
            formula = input("请输入大数1,大数2,Base,operation：").split(',')
            if len(formula)!=4 or formula[3] not in ['+','-','*']:
                print("输入有误，程序结束")
                break
        else:
            print('输入模式有误，请重新输入')
            break
        final_formula,err = Pretty(formula,mode)
        if err != 0:
            print(err)
            break;
        else:
            result = Calculate(final_formula, precision, mode)
            ViewResult(result, precision, mode)
