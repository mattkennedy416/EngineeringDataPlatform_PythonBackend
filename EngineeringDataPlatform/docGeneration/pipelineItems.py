

import glob
import json

print()


pythonPaths = glob.glob('../pipeline/*')

def parse_function_name(line):
    line = line.strip()
    funcNameStart = line.find('def ') + 4
    funcNAmeEnd = line.find('(', funcNameStart)
    funcName = line[funcNameStart:funcNAmeEnd].strip()

    return funcName

def parse_function_docstring(content):
    # ok now what's our format going to be to parse this?
    # - @tag = transforms.columns
    # - @config_params
    #     - name; required; valid values/types; examples
    # - @valid_input <- run pipeline validation on this
    # - @valid_output <- run pipeline validation on this
    # - @description = "blah blah"
    # - @working_example = config; input; output

    # want to spit this out to some markdown format, but also let us use it for pipeline validation
    # and what connections can be made between transforms

    func_name = parse_function_name(docstring_content[0])

    parameter_names = ['tag', 'config_params', 'valid_input', 'valid_output', 'description', 'working_example']
    parameter_vals = {'func_name': func_name}
    for content_line in docstring_content[1:]:
        for param in parameter_names:
            tag = '@' + param + '='
            if tag in content_line:
                # don't worry about supporting multi-line yet
                start = content_line.find(tag) + len(tag)
                val = content_line[start:]
                parameter_vals[param] = val
                break

    return parameter_vals


all_docs = []

for path in pythonPaths:

    #path = '../pipeline/transforms.py'
    try:
        with open(path, 'r') as f:
            content = f.read()
    except:
        print('could not read', path)
        continue

    lines = content.split('\n')



    start_n = None
    start_docstring_n = None
    end_n = None
    for n, line in enumerate(lines):
        if 'def ' in line:
            # check if this is a real function vs something in a string or the docs..
            if line[:line.find('def ')].strip() != "": # there's content before the def in the line, assume it's a docstring
                # note that this could easily break if there's a "def " etc in the comment block of a different function
                continue

            start_n = n
            start_docstring_n = None
            end_n = None
        elif start_n is not None and start_docstring_n is None and '"""' in line:
            start_docstring_n = n
        elif start_docstring_n is not None and end_n is None and '"""' in line:
            end_n = n

            docstring_content = lines[start_n:end_n+1]

            parsed = parse_function_docstring(docstring_content)
            all_docs.append(parsed)


    print()
    # I think we actually want to dump this as JSON (for now,) not a bunch of markdown files
    # lets restructure so that the tags are at the top level

output = {}
for item in all_docs:
    tag = item.get('tag', 'untagged')
    if tag in output:
        output[tag].append(item)
    else:
        output[tag] = [item]

with open('pipeline_item_docs.json', 'w') as f:
    json.dump(output, f, indent=2)











