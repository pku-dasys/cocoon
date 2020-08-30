import sys
sys.path.append("../../..")
import util

class YosysSynth():
    def __init__(self, design):
        self.params = dict()
        self.design = design

    def getObjHDL(self):
        obj_path = util.getObjPath(self.design, "Yosys")
        obj_hdl = obj_path + "/" + self.design.top_name + ".v"
        return obj_hdl

    def getObjSDC(self):
        obj_path = util.getObjPath(self.design, "Yosys")
        obj_sdc = obj_path + "/" + self.design.top_name + ".sdc"
        return obj_sdc

    def getRptGates(self):
        rpt_path = util.getRptPath(self.design, "Yosys")
        rpt_gates = rpt_path + "/" + "gates_synth.rpt"
        return rpt_gates

    def getRptTiming(self):
        rpt_path = util.getRptPath(self.design, "Yosys")
        rpt_timing = rpt_path + "/" + "timing_synth.rpt"
        return rpt_timing

    def getRptPower(self):
        rpt_path = util.getRptPath(self.design, "Yosys")
        rpt_power = rpt_path + "/" + "gates_synth.rpt"
        return rpt_power

    def setParams(self, param, optional):
        if self.params.get(param) is not None:
            self.params[param] = optional
        else:
            assert False, 'Unknown param'

    def config(self, design, tcl_file):
        rtl_file = util.getHDL(self.design)
        lib_file = util.getLib(self.design)
        #top_name = self.design.top_name
        hdl_path = util.getHDLPath(self.design, "Yosys")
        lib_path = util.getLibPath(self.design, "Yosys")

        tcl_path = util.getScriptPath(self.design, "Yosys")
        tcl = open(tcl_path + "/" + tcl_file + ".ys", 'w', encoding = 'utf-8')

        tcl.write('read -sv %s\n'%(hdl_path + "/" + rtl_file))
        tcl.write('hierarchy -top %s\n'%(self.design.top_name))
        tcl.write('proc; opt; techmap; opt\n')
        tcl.write('write_verilog %s\n'%(self.getObjHDL()))

        tcl.close()
