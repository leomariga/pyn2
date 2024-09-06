from pyn2.chart import Element, Group, N2

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
    