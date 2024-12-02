from SymbolTable import SymbolTable
from Scanner import Scanner

file = open("main.in", 'r')

st = SymbolTable()
scanner = Scanner(file=file, s_table=st)
