import os
import util


class InnovusRoute():
    def __init__(self, design):
        self.design = design
        self.params = dict()
        self.paramsExtern = dict()
        self.paramsPassive = dict()

        self.paramsExtern['def_in'] = False
        self.paramsExtern['def_out'] = True
        self.paramsExtern['detailed_place'] = False
        self.paramsExtern['cadence_version'] = '19'

        self.params['highFrequency'] = False
        self.params['viaPillarOpt'] = False
        self.paramsPassive['clockEco'] = False
        self.paramsPassive['trackOpt'] = False
        self.paramsPassive['idealClock'] = False
        self.paramsPassive['viaOpt'] = False
        self.paramsPassive['wireOpt'] = False
        self.paramsPassive['placementCheck'] = False
        self.paramsPassive['noPlacementCheck'] = False
        self.paramsPassive['globalDetail'] = False
        self.paramsPassive['detail'] = False
        self.params['passiveFill'] = False

    def setParams(self, param, value):
        if self.params.get(param) != None:
            self.params[param] = value
        elif self.paramsExtern.get(param) != None:
            self.paramsExtern[param] = value
        elif self.paramsPassive.get(param) != None:
            self.paramsPassive[param] = value
        else:
            assert False, 'Unknown param'
    
    def getObjHDL(self):
        obj_path = util.getObjPath(self.design)
        obj_hdl = os.path.join(obj_path, self.design.top_name + ".vh")
        return obj_hdl

    def getObjSDC(self):
        obj_path = util.getObjPath(self.design)
        obj_sdc = os.path.join(obj_path, self.design.top_name + ".sdc")
        return obj_sdc

    def getObjMMMC(self):
        obj_path = util.getObjPath(self.design)
        mmmc_path = os.path.join(obj_path, "flow.view")
        return mmmc_path

    def getDreamplaceDef(self):
        run_path = util.getRunPath(self.design,)
        obj_def = os.path.join(run_path, "%s_after_fp" % self.design.top_name, "%s_after_fp.gp.def" % self.design.top_name)
        return obj_def

    def config(self, design, tcl_file):
        tcl_path = util.getScriptPath(self.design)
        ret = 'routeDesign'
        for i in self.params:
            if self.params[i]:
                ret = ret + " -" + i

        assert not (self.paramsPassive['placementCheck'] and self.paramsPassive['noPlacementCheck']),\
            'Option -placementCheck and -noPlacementCheck are mutually exclusive.'
        assert not (self.paramsPassive['globalDetail'] and self.paramsPassive['detail']),\
            'Option -globalDetail and -detail are mutually exclusive.'

        if not self.params['passiveFill']:
            for i in self.paramsPassive:
                if self.paramsPassive[i]:
                    ret = ret + " -" + i

        tcl = open(os.path.join(tcl_path, tcl_file + ".tcl"), 'w', encoding='utf-8')

        if self.paramsExtern["def_in"]:
            #init design
            tcl.write("set init_mmmc_file %s\n" % self.getObjMMMC()) 
            tcl.write("set init_lef_file %s\n" % self.design.lef_input) 
            tcl.write("set init_verilog %s\n" % self.getObjHDL())  # need to specified
            tcl.write('set init_gnd_net "VSS"\n')
            tcl.write('set init_pwr_net "VDD"\n')
            tcl.write("init_design\n")
            # Load DEF
            tcl.write("defIn %s\n" % self.getDreamplaceDef())

        if self.paramsExtern['detailed_place']:
            if self.paramsExtern['cadence_version'] == '19':
                tcl.write("place_design\n")
            elif self.paramsExtern['cadence_version'] == '15':
                tcl.write("placeDesign\n")
            else:
                Exception("Invalid Cadence version\n")
        
        # Routing
        tcl.write(ret + "\n")

        if self.paramsExtern['def_out']:
            tcl.write('set dbgLefDefOutVersion 5.8\ndefOut -floorplan -netlist -routing %s.def\n' % self.design.top_name)
        
        tcl.close()

        return ret
