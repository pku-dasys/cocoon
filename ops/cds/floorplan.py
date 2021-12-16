import sys
sys.path.append("../..")
import util

class InnovusFloorplan():
    def __init__(self, design):
        self.params = dict()
        self.paramsExtern = dict()
        self.design = design
        self.paramsExtern["def_out"] = False

        self.params["adjustToSite"] = False
        self.params["coreMarginsBy"] = False
        self.params["dieSizeByIoHeight"] = False
        self.params["flip"] = False
        self.params["fplanOrigin"] = False
        self.params["noResize"] = False
        self.params["noSnapToGrid"] = False
        self.params["overlapSameSiteRow"] = False
        self.params["b"] = False
        self.params["r"] = False #"1.0 0.7 0.0 0.0 0.0 0.0"
        self.params["d"] = False
        self.params["s"] = False
        self.params["su"] = False
        self.params["keepShape"] = False
        self.params["site"] = False
        self.params["siteOnly"] = False

    def setParams(self, param, value):
        if self.params.get(param) != None:
            self.params[param] = value
        elif self.paramsExtern.get(param) != None:
            self.paramsExtern[param] = value
        else:
            assert False, 'Unknown param'

    def getObjHDL(self):
        obj_path = util.getObjPath(self.design, "Cadence")
        obj_hdl = obj_path + "/" + self.design.top_name + ".vh"
        return obj_hdl

    def getObjSDC(self):
        obj_path = util.getObjPath(self.design, "Cadence")
        obj_sdc = obj_path + "/" + self.design.top_name + ".sdc"
        return obj_sdc

    def getObjMMMC(self):
        obj_path = util.getObjPath(self.design, "Cadence")
        obj_mmmc = "{" + obj_path + "/" + util.getMmmc(self.design) + "}"
        return obj_mmmc

    def getLEF(self):
        lef_path = util.getLefPath(self.design, "Cadence")
        lef_file = lef_path + "/" + util.getLef(self.design)
        return lef_file

    def config(self, design, tcl_file):
        tcl_path = util.getScriptPath(self.design, "Cadence")
        obj_path = util.getObjPath(self.design, "Cadence")
        lef_path = util.getLefPath(self.design, "Cadence")

        # tcl_path = "."
        tcl = open(tcl_path + "/" + tcl_file + ".tcl", 'w', encoding='utf-8')
        #init design
        tcl.write("set init_mmmc_file %s\n" % self.getObjMMMC()) 
        tcl.write("set init_lef_file %s\n" % self.getLEF()) 
        tcl.write("set init_verilog %s\n" % self.getObjHDL())  # need to specified
        tcl.write('set init_gnd_net "VSS"\n')
        tcl.write('set init_pwr_net "VDD"\n')
        tcl.write("init_design\n")

        #floorplan
        tcl.write("floorPlan")
        for param in self.params:
            if (self.params[param] != False):
                tcl.write(" -%s %s"%(param, self.params[param]))
        tcl.write("\n")

        if self.paramsExtern["def_out"]:
            # tcl.write("set dbgLefDefOutVersion 5.8\ndefOut -netlist %s_after_fp.def\n" % self.design.top_name)
            tcl.write("defOut -netlist %s_after_fp.def\n" % self.design.top_name)

        tcl.close()