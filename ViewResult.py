'''
查看运算结果模块
设计模式：Observer
功能：将运算结果以2、8、10、16进制输出
'''
from __future__ import annotations
from contextlib import suppress
from BaseChange import BaseChange


# Observer类：观察者
class Observer(object):
    def __init__(self, name:str):
        super(Observer, self).__init__()
        self.name = name
        # print("观察者", self.name, "已创建")

    def update(self, subject: Subject) -> None:
        pass


# SmallNumObserver类：实现SmallNumObserver类，普通数字观察者
class SmallNumObserver(Observer):
    def __init__(self, name, precision):
        super(Observer, self).__init__()
        self.name = name
        self.precision=precision
        # print("观察者", self.name, "已创建")


# BigNumObserver类：实现SmallNumObserver类，大数观察者
class BigNumObserver(Observer):
    pass


# BINViewer类，实现SmallNumObserver类，以二进制查看
class BINViewer(SmallNumObserver):
    def update(self, subject: SmallNumResult) -> None:
        print("二进制", subject.name, "为", BaseChange(subject.data, 10, 2, self.precision))


# OCTViewer类，实现SmallNumObserver类，以八进制查看
class OCTViewer(SmallNumObserver):
    def update(self, subject: SmallNumResult) -> None:
        print("八进制", subject.name, "为", BaseChange(subject.data, 10, 8, self.precision))


# DECViewer类，实现SmallNumObserver类，以十进制查看
class DECViewer(SmallNumObserver):
    def update(self, subject: SmallNumResult) -> None:
        print("十进制", subject.name, "为", BaseChange(subject.data, 10, 10, self.precision))


# HEXViewer类，实现SmallNumObserver类，以十六进制查看
class HEXViewer(SmallNumObserver):
    def update(self, subject: SmallNumResult) -> None:
        print("十六进制", subject.name, "为", BaseChange(subject.data, 10, 16, self.precision))


# BigNumViewer类：实现BigNumObserver类，查看大数
class BigNumViewer(BigNumObserver):
    def update(self, subject: BigNumResult) -> None:
        print(subject.name+"为:", end='')
        i = len(subject.data)-2
        j = 0
        while(j<i):
            print(subject.data[j]+f"*{subject.data[-1]}"*(i-j),end='+')
            j=j+1
        print(subject.data[-2])


# Subject类：被观察者
class Subject(object):
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            # print("观察者", observer.name, "正在观察", self.name)

    def detach(self, observer: Observer) -> None:
        with suppress(ValueError):
            self._observers.remove(observer)
            # print("观察者", observer.name, "解除观察", self.name)

    def notify(self, modifier: Observer | None = None) -> None:
        for observer in self._observers:
            if modifier != observer:
                # print(self.name, "已通知观察者", observer.name)
                observer.update(self)


# SmallNumResult类：实现Subject类，普通模式运算结果
class SmallNumResult(Subject):
    def __init__(self, name: str = "") -> None:
        super().__init__()
        self.name = name
        self._data = 0.0

    @property
    def data(self) -> float:
        return self._data

    @data.setter
    def data(self, value: float) -> None:
        self._data = value
        self.notify()


# BigNumResult类：实现Subject类，大数模式运算结果
class BigNumResult(Subject):
    def __init__(self, name: str = "") -> None:
        super().__init__()
        self.name = name
        self._data = []

    @property
    def data(self) -> list:
        return self._data

    @data.setter
    def data(self, value: list) -> None:
        self._data = value
        self.notify()


def ViewResult(data:float|list, precision:int=100, mode:int=1) -> None:
    if mode == 1:
        result = SmallNumResult("运算结果")
        binviewer = BINViewer("二进制格式",precision)
        octviewer = OCTViewer("八进制格式",precision)
        decviewer = DECViewer("十进制格式",precision)
        hexviewer = HEXViewer("十六进制格式",precision)
        result.attach(binviewer)
        result.attach(octviewer)
        result.attach(decviewer)
        result.attach(hexviewer)
        result.data = data
    elif mode in [2,3]:
        result = BigNumResult("运算结果")
        bignumviewer = BigNumViewer("大数格式")
        result.attach(bignumviewer)
        result.data = data