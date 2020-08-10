import sys
sys.path.append("../..")
import util

class Params():
    def __init__(self, typ, name, value, optional = False):
        self.type = typ
        self.name = name
        self.range = []
        self.value = value
        self.optional = optional

    def check_valid(self):
        return True

class GenusSynth():
    def __init__(self, design):
        self.params = dict()
        self.params["effort"] = "medium"
        self.params["is_incremental"] = True
        self.params["spatial"] = False
        self.design = design
        #self.design.obj_hdl = design.obj_path + "/" + design.top_name + ".vh"
        #self.design.obj_sdc = design.obj_path + "/" + design.top_name + "_synth.sdc"
        #self.design.rpt_gates = design.rpt_path + "/" + "gates_synth.rpt"
        #self.design.rpt_timing = design.rpt_path + "/" + "timing_synth.rpt"
        #self.design.rpt_power = design.rpt_path + "/" + "power_synth.rpt"

    def getObjHDL(self):
        obj_path = util.getObjPath(self.design, "Cadence")
        obj_hdl = obj_pat + "/" + self.design.top_name + ".vh"
        return obj_hdl

    def getObjSDC(self):
        obj_path = util.getObjPath(self.design, "Cadence")
        obj_sdc = obj_pat + "/" + self.design.top_name + "_synth.sdc"
        return obj_sdc

    def getRptGates(self):
        rpt_path = util.getRptPath(self.design, "Cadence")
        rpt_gates = rpt_path + "/" + "gates_synth.rpt"
        return rpt_gates

    def getRptTiming(self):
        rpt_path = util.getRptPath(self.design, "Cadence")
        rpt_timing = rpt_path + "/" + "timing_synth.rpt"
        return rpt_timing

    def getRptGates(self):
        rpt_path = util.getRptPath(self.design, "Cadence")
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
        hdl_path = util.getHDLPath(self.design, "Cadence")
        lib_path = util.getLibPath(self.design, "Cadence")

        #tcl = open(tcl_file + ".tcl", 'w', encoding='utf-8')
        tcl_path = util.getScriptPath(self.design, "Cadence")
        print(tcl_path)
        tcl = open(tcl_path + "/" + tcl_file + ".tcl", 'w', encoding='utf-8')

        #tcl.write('set hdl_files %s\n'%(self.design.rtl_file))
        tcl.write('set hdl_files %s\n'%(rtl_file))
        tcl.write('set DESIGN %s\n'%(self.design.top_name))
        tcl.write('set clkpin %s\n'%(self.design.clk_name))
        tcl.write('set delay %d\n'%(self.design.delay))
        #tcl.write('set_attribute hdl_search_path %s\n'%(self.design.hdl_path))
        #tcl.write('set_attribute lib_search_path %s\n'%(self.design.lib_path))
        tcl.write('set_attribute hdl_search_path %s\n'%(shdl_path))
        tcl.write('set_attribute lib_search_path %s\n'%(lib_path))
        tcl.write('set_attribute information_level 6 \n')
        tcl.write('set_attribute library %s\n'%(lib_file))
        tcl.write('read_hdl ${hdl_files} \n')
        tcl.write('elaborate $DESIGN \n')
        tcl.write('set clock [define_clock -period ${delay} -name ${clkpin} [clock_ports]]\n')
        tcl.write('external_delay -input   0 -clock clk [find / -port ports_in/*]\n')
        tcl.write('external_delay -output  0 -clock clk [find / -port ports_out/*]\n')
        tcl.write('dc::set_clock_transition .4 clk\n')
        tcl.write('check_design -unresolved\n')
        tcl.write('report timing -lint\n')

        ret = 'synthesize'

        for i in self.params:
            if self.params[i]:
                ret = ret + " -" + i
        
        tcl.write(ret + '\n')

        #tcl.write("report timing > %s\n"%(self.design.rpt_timing))
        #tcl.write('report gates  > %s\n'%(self.design.rpt_gates))
        #tcl.write('report power  > %s\n'%(self.design.rpt_power))
        #tcl.write('write_hdl -mapped >  %s\n'%(self.design.obj_hdl))
        #tcl.write('write_sdc >  %s\n'%(self.design.obj_sdc))

        tcl.write("report timing > %s\n"%(self.getRptTiming()))
        tcl.write('report gates  > %s\n'%(self.getRptGates()))
        tcl.write('report power  > %s\n'%(self.getRptPower()))
        tcl.write('write_hdl -mapped >  %s\n'%(self.getObjHDL()))
        tcl.write('write_sdc >  %s\n'%(self.getObjSDC()))

        tcl.close()

class Output(object):

    def __init__(self, design):
        pass

    def config(self, file_name):
        f = open(file_name + ".tcl", "w")
        # to-do
        f.close()
