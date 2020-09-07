import sys
sys.path.append("../..")
import util

class InnovusCTS(object):
    def __init__(self, design):
        self.design = design
        self.params = dict()
        self.params['check_prerequisites'] = False
        self.params['ckSpec'] = False
        self.params['cts'] = False
        self.params['expandedViews'] = False
        
        self.outDir = "!"
        self.prefix = "!"

    def setParam(self, param, strParam = "DASYS"):
        if param == 'outDir':
            self.outDir = strParam
        elif param == 'prefix':
            self.prefix = strParam
        elif self.params.get(param) == None:
            print('[error] unknown param')
        else:
            self.params[param] = True
        
    def config(self, design, tcl_file):
        tcl_path = util.getScriptPath(self.design, "Cadence")
        ret = 'ccopt_design'
        if self.outDir != '!':
            ret = ret + ' -outDir ' + self.outDir
        if self.prefix != '!':
            ret = ret + ' -prefix ' + self.prefix
        for i in self.params:
            if self.params[i] == True:
                ret = ret + ' -' + i
        
        tcl = open(tcl_path + "/" + tcl_file + ".tcl", 'w', encoding='utf-8')
        tcl.writelines(ret)
        tcl.close()
        return ret