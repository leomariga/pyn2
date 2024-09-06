from openmdao.visualization.htmlpp import HtmlPreprocessor
import openmdao
import json
import os
import inspect 
import sys

class Element:
    def __init__(self, name, color='black') -> None:
        self.name = name
        self.color = color
        self.connections = []
        self.parent = None

    def connect_to(self, e: 'Element'):
        self.connections.append(e)

class Group:
    def __init__(self, name) -> None:
        self.name = name
        self.children = []
        self.parent = None

    def add_element(self, element: Element):
        element.parent = self
        self.children.append(element)

    def add_group(self, group: 'Group'):
        group.parent = self
        self.children.append(group)

class N2:

    def __init__(self, name: str = 'root')  -> None:
        self.children: list = []
        self.name = name
        self.parent = None
        
    def add_element(self, element: Element):
        self.children.append(element)

    def add_group(self, group: Group):
        group.parent = self
        self.children.append(group)

    def generate_report(self):
        def _get_element_dict(e: Element):
            e_dict = {
                'name': f'{e.name}',
                'type': 'input',
                'value': 0
            }
            return e_dict

        def _get_group_dict(g: Group):
            g_dict = {
                'name': f'{g.name}',
                'type': 'group',
                'children': []
            }
            for c in g.children:
                if isinstance(c, Group):
                    c_dict = _get_group_dict(c)
                    g_dict['children'].append(c_dict)
                elif isinstance(c, Element):
                    c_dict = _get_element_dict(c)
                    g_dict['children'].append(c_dict)
                else:
                    raise(Exception('Cant reconize type for children. Use only Group or Element'))
            return g_dict
        
        def _get_trace_element(e: Element):
            trace = f'{e.name}'
            if e.parent:
                parent_element = e
                while parent_element.parent:
                    parent_element = parent_element.parent
                    if parent_element.parent:
                        trace = f'{parent_element.name}.{trace}'
                    
            return trace

        def _get_connections_dict(g: Group):
            con_list = []
            for c in g.children:
                if isinstance(c, Group):
                    con_subgroup = _get_connections_dict(c)
                    con_list.extend(con_subgroup)
                elif isinstance(c, Element):
                    if len(c.connections) != 0:
                        for dst_element in c.connections:
                            con_list.append({ 'src': _get_trace_element(c), 'tgt': _get_trace_element(dst_element)})
                else:
                    raise(Exception('Cant reconize type for children. Use only Group or Element'))
            return con_list

        model_data = {}
        root = Group(self.name)
        root.children = self.children
        model_data['tree'] = _get_group_dict(root)
        default_output_filename = 'gen_diag.html'

        con_list = _get_connections_dict(root)
        model_data['connections_list'] = tuple(con_list)

        pretty = json.dumps(model_data, indent=2)
        print(pretty)
        

        title = "Generic model diagram"

        html_vars = {
            'title': title,
            'embeddable': "non-embedded-diagram",
            'sw_version': 0.1,
            'model_data': model_data
        }


        openmdao_dir = os.path.dirname(inspect.getfile(openmdao))
        vis_dir = os.path.join(openmdao_dir, "visualization/n2_viewer")

        HtmlPreprocessor(os.path.join(vis_dir, "tests/gen_test.html"), default_output_filename,
                            search_path=[vis_dir], allow_overwrite=True, var_dict=html_vars,
                            verbose=False).run()


if __name__ == '__main__':
    n2 = N2('test_chart')
    s_dev = Group('Software_development')
    e_analyze = Element('Analyze')
    e_code = Element('Code')
    e_build = Element('Build')
    e_deploy = Element('Deploy')
    
    t_vnv = Group('Software_vnv')
    e_review = Element('Review')
    e_test = Element('Test')

    e_analyze.connect_to(e_code)
    e_code.connect_to(e_build)
    e_code.connect_to(e_review)
    e_review.connect_to(e_analyze)
    e_build.connect_to(e_test)
    e_test.connect_to(e_deploy)
    e_test.connect_to(e_analyze)

    s_dev.add_element(e_analyze)
    s_dev.add_element(e_code)
    s_dev.add_element(e_build)
    s_dev.add_element(e_deploy)

    t_vnv.add_element(e_review)
    t_vnv.add_element(e_test)

    n2.add_group(s_dev)
    n2.add_group(t_vnv)
    n2.generate_report()
    