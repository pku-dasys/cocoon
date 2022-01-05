import os
import util

class InnovusDRC():
    def __init__(self, design):
        self.design = design
        self.params = dict()
        self.params['out_file'] = 'default'
        self.params['no_check'] = False
        self.params['type'] = "all"

    def setParams(self, param, value):
        if self.params.get(param) is not None:
            self.params[param] = value
        else:
            assert False, 'Unknown param'

    def config(self, design, tcl_file):
        tcl_path = util.getScriptPath(self.design)
        ret = 'check_design'
        if self.params['out_file'] != 'default':
            ret = ret + " -out_file " + self.params['out_file']

        if self.params['no_check']:
            ret = ret + " -no_check"
        else:
            ret = ret + " -type " + self.params['type']

        tcl = open(os.path.join(tcl_path, tcl_file + ".tcl"), 'w', encoding='utf-8')
        tcl.writelines(ret)
        tcl.close()

        return ret