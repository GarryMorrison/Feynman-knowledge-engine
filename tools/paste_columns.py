#!/usr/bin/env python3


def normalize_column_return_list(s,n):
  lines = (s.split('\n') + ['']*n)[:n]
  max_len = max(len(x) for x in lines)
  return [x.ljust(max_len) for x in lines]


def paste_columns(data,pre='',sep=' ',post=''):
  if len(data) == 0:
    return ""
  columns = len(data)
  rows = max(s.count('\n') + 1 for s in data)
  r = [normalize_column_return_list(s,rows) for s in data]
  return "\n".join(pre + sep.join(r[j][k] for j in range(columns)) + post for k in range(rows))



x_vect = "x1\nx2\nx3\nx4\nx5\nx6"
y_vect = "y1\ny2\ny3"
z_vect = "z1\nz2\nz3\nz4"
equal = "="


col_1 = "7\n1\n9\n14"
col_2 = "6\n1\n13\n10"
col_3 = "14\n19\n13\n4"
col_4 = "12\n16\n10\n14"
col_5 = "10\n0\n12\n6"
col_6 = "10\n14\n3\n16"
matrix1 = paste_columns([col_1,col_2,col_3,col_4,col_5,col_6],'[ ',' ',' ]')


col_1 = "0.25\n4\n-7"
col_2 = "1020\n0\n5.37"
col_3 = "1\n-2\n4.1"
col_4 = "3\n5\n13"

matrix2 = paste_columns([col_1,col_2,col_3,col_4],'[ ',' ',' ]')


x = paste_columns([x_vect],'[ ','',' ]')
y = paste_columns([y_vect],'[ ','',' ]')
z = paste_columns([z_vect],'[ ','',' ]')

r1 = paste_columns([z,equal,matrix1,x])
r2 = paste_columns([y,equal,matrix2,matrix1,x])



print(matrix1,'\n')
print(matrix2,'\n')
print(x,'\n')
print(y,'\n')
print(z,'\n')

print(r1,'\n')
print(r2,'\n')


col_1 = "kuro5hin\ndiary"
col_2 = "a\nb\nc\nd\ne\nf"
col_3 = "x\ny\nz\n\ntext"

table = paste_columns([col_1,col_2,col_3],"| "," | "," |")
print(table)


s1 = """
x = paste_columns([x_vect],'[ ','',' ]')
y = paste_columns([y_vect],'[ ','',' ]')
z = paste_columns([z_vect],'[ ','',' ]')
"""

s2 = """
r1 = paste_columns([z,equal,matrix1,x])
r2 = paste_columns([y,equal,matrix2,matrix1,x])
"""

table = paste_columns([s1,s2],'','   ','')
print(table)


s1 = """
def normalize_column_return_list(s,n):
  lines = (s.split('\\n') + ['']*n)[:n]
  max_len = max(len(x) for x in lines)
  return [x.ljust(max_len) for x in lines]
"""

s2 = """
def paste_columns(data,pre='',sep=' ',post=''):
  columns = len(data)
  rows = max(s.count('\\n') + 1 for s in data)
  r = [normalize_column_return_list(s,rows) for s in data]
  return "\\n".join(pre + sep.join(r[j][k] for j in range(columns)) + post for k in range(rows))
"""

table = paste_columns([s1,s2],'','   ','')
print(table)

