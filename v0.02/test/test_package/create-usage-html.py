#!c:/Python34/python.exe 

#######################################################################
# convert console usage information into html
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 18/3/2018
# Update: 25/3/2018
# Copyright: GPLv3
#
# Usage: ./create-usage-html.py
#
#######################################################################

import os
import glob
import shutil
import datetime
from re import sub


from semantic_db.usage_tables import built_in_table_usage, sigmoid_table_usage, examples_usage
from semantic_db.functions import function_operators_usage, sequence_functions_usage


def create_directory(dir):
    try:
        if not os.path.exists(dir):
            print("Creating %s directory." % dir)
            os.makedirs(dir)
    except Exception as e:
        print('Failed to create directory: %s\nReason: %s' % (dir, e))


def save_file(name, text):
    try:
        with open(name, 'w') as file:
            print('saving file: %s' % name)
            file.write(text)
    except Exception as e:
        print('Failed to create %s\nReason: %s' % (name, e))


def load_usage_info():
    op_type = {}
    location = {}
    usage = {}
    for key in built_in_table_usage:
        op_type[key] = 'built in operator'
        location[key] = 'built-in'
        usage[key] = built_in_table_usage[key]

    for key in sigmoid_table_usage:
        op_type[key] = 'sigmoid'
        location[key] = 'sigmoids'
        usage[key] = sigmoid_table_usage[key]

    for key in function_operators_usage:
        op_type[key] = 'operator'
        location[key] = 'function-operators'
        usage[key] = function_operators_usage[key]

    for key in sequence_functions_usage:
        op_type[key] = 'sequence function'
        location[key] = 'sequence-functions'
        usage[key] = sequence_functions_usage[key]

    for key in examples_usage:
        op_type[key] = 'worked example'
        location[key] = 'worked-examples'
        usage[key] = examples_usage[key]

    return op_type, location, usage


def single_usage_to_html(op_name, op_type, location, usage, sw_files):
    header = """
<html>
<head><title>%s: %s</title></head>
<body>
<h3>%s: %s</h3>
""" % (op_type[op_name], op_name, op_type[op_name], op_name)
    footer = """
<hr>
<a href="../index.html">Home</a><br>
</body>
</html>    
"""
    text = usage[op_name]
    for op in location:             # is there a cleaner way to do this?
        text = text.replace(' %s ' % op, ' <a href="../%s/%s.html">%s</a> ' % (location[op], op, op))
        text = text.replace(' %s[' % op, ' <a href="../%s/%s.html">%s</a>[' % (location[op], op, op))
        text = text.replace(' %s(' % op, ' <a href="../%s/%s.html">%s</a>(' % (location[op], op, op))
        text = text.replace('(%s ' % op, '(<a href="../%s/%s.html">%s</a> ' % (location[op], op, op))
        text = text.replace(' %s,' % op, ' <a href="../%s/%s.html">%s</a>,' % (location[op], op, op))
        text = text.replace(' %s\n' % op, ' <a href="../%s/%s.html">%s</a>\n' % (location[op], op, op))
        text = text.replace(' %s^' % op, ' <a href="../%s/%s.html">%s</a>^' % (location[op], op, op))
    for base_name in sw_files:
        text = text.replace('load %s' % base_name, 'load <a href="../sw-examples/%s">%s</a>' % (base_name, base_name))
    regex = r"web-load http://(.*)\.sw"
    text = sub(regex, r"web-load <a href='http://\1.sw'>http://\1.sw</a>", text)
    s = '<pre>%s</pre>' % text
    return header + s + footer


def create_index_html_page(location, sw_files, dot_files):
    header = """
<html>
<head><title>Semantic DB usage information</title></head>
<body>
<h3>Semantic DB usage information</h3>
Welcome to the Semantic DB usage page. Below are brief descriptions and examples for our operators and sequence functions.
"""
    footer = """
<hr>
updated: %s<br>
by Garry Morrison<br>
email: garry -at- semantic-db.org
</body>
</html>    
""" % datetime.date.today().strftime("%B %d, %Y")

    s = '<dl>\n'
    s += '  <dt><b>built in operators:</b></dt>\n'
    for key in sorted(built_in_table_usage):
        s += '    <dd><a href="%s/%s.html">%s</a></dd>\n' % (location[key], key, key)
    s += '</dl>\n'

    s += '<dl>\n  <dt><b>sigmoids:</b></dt>\n'
    for key in sorted(sigmoid_table_usage):
        s += '    <dd><a href="%s/%s.html">%s</a></dd>\n' % (location[key], key, key)
    s += '</dl>\n'

    s += '<dl>\n  <dt><b>operators:</b></dt>\n'
    for key in sorted(function_operators_usage):
        s += '    <dd><a href="%s/%s.html">%s</a></dd>\n' % (location[key], key, key)
    s += '</dl>\n'

    s += '<dl>\n  <dt><b>sequence functions:</b></dt>\n'
    for key in sorted(sequence_functions_usage):
        s += '    <dd><a href="%s/%s.html">%s</a></dd>\n' % (location[key], key, key)
    s += '</dl>\n'

    s += '<dl>\n  <dt><b>worked examples:</b></dt>\n'
    for key in sorted(examples_usage):
        s += '    <dd><a href="%s/%s.html">%s</a></dd>\n' % (location[key], key, key)
    s += '</dl>\n'

    s += '<dl>\n  <dt><b>sw examples:</b></dt>\n'
    for key in sorted(sw_files):
        s += '    <dd><a href="sw-examples/%s">%s</a></dd>\n' % (key, key)
    s += '</dl>\n'

    s += '<dl>\n  <dt><b>graph examples:</b></dt>\n'
    for key in sorted(dot_files):
        s += '    <dd><a href="graph-examples/%s">%s</a></dd>\n' % (key, key)
    s += '</dl>\n'
    return header + s + footer


def main():
    create_directory('documentation/usage')
    os.chdir('documentation/usage/')
    create_directory('built-in')
    create_directory('sigmoids')
    create_directory('function-operators')
    create_directory('sequence-functions')
    create_directory('worked-examples')
    create_directory('sw-examples')
    create_directory('graph-examples')

    sw_files = []
    for sw_file in (glob.glob("../../sw-examples/*.swc") + glob.glob("../../sw-examples/*.sw")):
        shutil.copy2(sw_file, 'sw-examples')
        base_name = os.path.basename(sw_file)
        print('Copied file: %s' % base_name)
        sw_files.append(base_name)

    dot_files = []
    for dot_file in (glob.glob("../../graph-examples/*.dot") + glob.glob("../../graph-examples/*.png")):
        shutil.copy2(dot_file, 'graph-examples')
        base_name = os.path.basename(dot_file)
        print('Copied file: %s' % base_name)
        dot_files.append(base_name)

    op_type, location, usage = load_usage_info()
    h = create_index_html_page(location, sw_files, dot_files)
    save_file('index.html', h)

    for op in location:
        h = single_usage_to_html(op, op_type, location, usage, sw_files)
        dest = '%s/%s.html' % (location[op], op)
        save_file(dest, h)


main()
