# encoding=utf-8
from bs4 import BeautifulSoup

# 页面模块解析封装


class AnalysisPage:
    def __init__(self, html, **kwargs):
        self.html = html

    def analysishtml(self):
        soup = BeautifulSoup(self.html)
        return soup
