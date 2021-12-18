import os
import util


class InnovusPDN():
    def __init__(self, design):
        self.params = dict()
        self.design = design

    def setParams(self, param, optional):
        if self.params.get(param) is not None:
            self.params[param] = optional
        else:
            assert False, 'Unknown param'

    def config(self, design, tcl_file):
        tcl_path = util.getScriptPath(self.design)
        tcl = open(os.path.join(tcl_path, tcl_file + ".tcl"), 'w', encoding='utf-8')

        tcl.write('globalNetConnect VDD -type pgpin -pin VDD -inst * -verbose\n')
        tcl.write('globalNetConnect VSS -type pgpin -pin VSS -inst * -verbose\n')
        tcl.write('sroute -nets {VDD VSS}\n')
        tcl.write('addRing -nets {VDD VSS} -width 0.6 -spacing 0.5 -layer [list top 7 bottom 7 left 6 right 6]\n')
        tcl.write('addStripe -nets {VSS VDD} -layer 6 -direction vertical -width 0.4 -spacing 0.5 -set_to_set_distance 5 -start 0.5\n')
        tcl.write('addStripe -nets {VSS VDD} -layer 7 -direction horizontal -width 0.4 -spacing 0.5 -set_to_set_distance 5 -start 0.5\n')

        tcl.close()