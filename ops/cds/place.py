import sys
sys.path.append("../..")
import util

class InnovusPlace(object):
    def __init__(self, design):
        self.design = design
        self.params = dict()
        self.params['concurrent_macros'] = False
        self.params['incremental'] = False
        self.params['noPrePlaceOpt'] = False
        
    def setParams(self, param):
        if self.params.get(param) == None:
            print('[error] unknown param')
        else:
            self.params[param] = True
    
    def config(self, design, tcl_file):
        tcl_path = util.getScriptPath(self.design, "Cadence")
        ret = 'place_design'
        for i in self.params:
            if self.params[i] == True:
                ret = ret + " -" + i
        
        tcl = open(tcl_path + "/" + tcl_file + ".tcl", 'w', encoding = 'utf-8')
        tcl.writelines(ret)
        tcl.close()

        return ret