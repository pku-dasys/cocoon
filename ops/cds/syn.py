import os
import util


class GenusSynth:
    def __init__(self, design, critical_path=None):
        self.params = dict()
        self.params["effort"] = "medium"
        self.params["is_incremental"] = True
        self.params["spatial"] = False
        self.critical_path = critical_path
        self.design = design

    def getObjHDL(self):
        obj_path = util.getObjPath(self.design)
        obj_hdl = os.path.join(obj_path, self.design.top_name + ".vh")
        return obj_hdl

    def getObjSDC(self):
        obj_path = util.getObjPath(self.design)
        obj_sdc = os.path.join(obj_path, self.design.top_name + ".sdc")
        return obj_sdc

    def getRptGates(self):
        rpt_path = util.getRptPath(self.design)
        rpt_gates = os.path.join(rpt_path, "gates_synth.rpt")
        return rpt_gates

    def getRptTiming(self):
        rpt_path = util.getRptPath(self.design)
        rpt_timing = os.path.join(rpt_path, "timing_synth.rpt")
        return rpt_timing

    def getRptPower(self):
        rpt_path = util.getRptPath(self.design)
        rpt_power = os.path.join(rpt_path, "power_synth.rpt")
        return rpt_power

    def setParams(self, param, optional):
        if self.params.get(param) is not None:
            self.params[param] = optional
        else:
            assert False, 'Unknown param'
    
    def pathGroup(self):
        cmd = '\n'
        if self.critical_path:
            fields_start = [('reg', '[all_registers]', 'C'), 
                           ('io', '[all_inputs]', 'I'),
                           ('in', '[all_inputs]', 'I')]
            fields_end = [('reg', '[all_registers]', 'C'), 
                           ('io', '[all_outputs]', 'O'),
                           ('out', '[all_outputs]', 'O')]
            (_start, _end) = self.critical_path
            _start.lower()
            _end.lower()
            start_index, end_index = 0, 0
            for i, field in enumerate(fields_start):
                if field[0] in _start:
                    start_index = i
                    break
            for i, field in enumerate(fields_end):
                if field[0] in _end:
                    end_index = i
                    break
            name = "%s2%s" % (fields_start[start_index][2], fields_end[end_index][2])
            cmd = "define_cost_group -name %s -design $DESIGN\n" % name
            cmd += "path_group -from %s -to %s -group %s -name %s\n" % (fields_start[start_index][1], fields_end[end_index][1], name, name)

        return cmd

    def config(self, tcl_name):
        rtl_file = self.design.rtl_input
        lib_file = self.design.liberty_input
        tcl_path = util.getScriptPath(self.design)
        tcl = open(os.path.join(tcl_path, tcl_name + ".tcl"), 'w', encoding='utf-8')

        tcl.write('set DESIGN %s\n'%(self.design.top_name))
        tcl.write('set clkpin %s\n'%(self.design.clk_name))
        tcl.write('set delay %d\n'%(self.design.delay))
        
        tcl.write('set_attribute information_level 6 \n')
        tcl.write('set_attribute library %s\n'%(lib_file))
        tcl.write(f'read_hdl {rtl_file}\n')

        tcl.write('elaborate $DESIGN \n')

        # Path group for timing optimization
        tcl.write(self.pathGroup())

        tcl.write('set clock [define_clock -period ${delay} -name ${clkpin} [clock_ports]]\n')
        tcl.write('external_delay -input   0 -clock clk [find / -port ports_in/*]\n')
        tcl.write('external_delay -output  0 -clock clk [find / -port ports_out/*]\n')
        tcl.write('dc::set_clock_transition .4 clk\n')
        tcl.write('check_design -unresolved\n')
        tcl.write('report timing -lint\n')

        ret = 'synthesize -to_mapped'

        for i in self.params:
            if self.params[i]:
                ret = ret + " -" + i
        
        tcl.write(ret + '\n')

        tcl.write("report timing > %s\n"%(self.getRptTiming()))
        tcl.write('report gates  > %s\n'%(self.getRptGates()))
        tcl.write('report power  > %s\n'%(self.getRptPower()))
        tcl.write('write_hdl -mapped >  %s\n'%(self.getObjHDL()))
        tcl.write('write_sdc >  %s\n'%(self.getObjSDC()))

        tcl.close()


class YosysSynth:

    def __init__(self, design):
        self.design = design
    
    def getObjHDL(self):
        obj_path = util.getObjPath(self.design)
        obj_hdl = os.path.join(obj_path, self.design.top_name + ".vh")
        return obj_hdl

    def getObjSDC(self):
        obj_path = util.getObjPath(self.design)
        obj_sdc = os.path.join(obj_path, self.design.top_name + ".sdc")
        return obj_sdc

    def writeSDC(self):
        sdc = open(self.getObjSDC(), 'w', encoding='utf-8')
        sdc.write("set sdc_version 2.0\n")
        sdc.write(f"current_design {self.design.top_name}\n")
        sdc.write(f'create_clock -name "{self.design.clk_name}" -period {0.001 * self.design.delay} ' + '-waveform {0.0 0.05}\n')
        sdc.close()

    def config(self, tcl_name, flow):
        rtl_file = self.design.rtl_input
        lib_file = self.design.liberty_input
        tcl_path = util.getScriptPath(self.design)
        tcl = open(os.path.join(tcl_path, tcl_name + ".ys"), 'w', encoding='utf-8')

        tcl.write("# Synthesis script for yosys created by qflow\n")
        tcl.write(f"read_liberty -lib -ignore_miss_dir -setattr blackbox {lib_file}\n")
        tcl.write(f"read_verilog {rtl_file}\n\n")
        tcl.write("# High-level synthesis\n")
        tcl.write(f"synth -top {self.design.top_name}\n")
        tcl.write(f"dfflibmap -liberty {lib_file}\nopt\n\n")

        abc_path = os.path.join(flow.yosys_bin_path, "yosys-abc")
        tcl.write(f"abc -exe {abc_path} -liberty {lib_file} " + "-script +strash;scorr;ifraig;retime,{D};strash;dch,-f;map,-M,1,{D}\n")
        tcl.write("flatten\nsetundef -zero\nclean -purge\niopadmap -outpad BUFX2 A:Y -bits\n")
        tcl.write("opt\nclean\nrename -enumerate\n")
        tcl.write(f"write_verilog {self.getObjHDL()}\n")
        tcl.write("stat\n")

        tcl.close()

        self.writeSDC()
