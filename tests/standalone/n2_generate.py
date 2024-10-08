from openmdao.visualization.htmlpp import HtmlPreprocessor
import json
import os
import inspect 
import sys

default_output_filename = 'gen_diag.html' if len(sys.argv) < 2 else sys.argv[1]

model_data = {
    'tree': {
        'name': 'root',
        'type': 'group',
        'children': []
    }
}

tree=model_data['tree']

for x in range (1,3):
    newchild0 = {
        'name': f'grp_{(x)}',
        'type': 'group',
        'children': []
    }

    tree['children'].append(newchild0)
    ch0 = newchild0['children']
    for y in range (1,5):
        newchild1 = {
            'name': f'child_{(y)}',
            'type': 'group',
            'children': []
        }
        ch1 = newchild1['children']
        ch0.append(newchild1)

        for z in range (1,4):
            newchild2 = {
                'name': f'input_{y}_{z}',
                'type': 'input',
                'val': 1000 * z + 10 * y + x
            }
            ch1.append(newchild2)

            newchild3 = {
                'name': f'output_{y}_{z}',
                'type': 'output',
                'val': 1111 * z + 20 * y + x
            }
            ch1.append(newchild3) 

model_data['connections_list'] = (
    { 'src': 'grp_1.child_1.output_1_1', 'tgt': 'grp_1.child_2.input_2_1'},
    { 'src': 'grp_1.child_2.output_2_2', 'tgt': 'grp_2.child_1.input_1_2'},
    { 'src': 'grp_1.child_3.output_3_1', 'tgt': 'grp_2.child_3.input_4_1'},
    { 'src': 'grp_1.child_1.output_1_2', 'tgt': 'grp_2.child_2.input_2_1'},
    { 'src': 'grp_2.child_2.output_2_1', 'tgt': 'grp_1.child_2.input_2_1'},
    
)

# pretty = json.dumps(model_data, indent=2)
# print(pretty)
# exit

title = "Generic model diagram"

html_vars = {
    'title': title,
    'embeddable': "non-embedded-diagram",
    'sw_version': 0.1,
    'model_data': model_data
}

import openmdao
openmdao_dir = os.path.dirname(inspect.getfile(openmdao))
vis_dir = os.path.join(openmdao_dir, "visualization/n2_viewer")

HtmlPreprocessor(os.path.join(vis_dir, "tests/gen_test.html"), default_output_filename,
                    search_path=[vis_dir], allow_overwrite=True, var_dict=html_vars,
                    verbose=False).run()

