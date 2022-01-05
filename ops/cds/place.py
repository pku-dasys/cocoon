import os
import util
import json
import collections


class InnovusPlace(object):
    def __init__(self, design):
        self.design = design
        self.params = dict()
        self.params['concurrent_macros'] = False
        self.params['incremental'] = False
        self.params['noPrePlaceOpt'] = False
        self.params['cadence_version'] = '19'
        
    def setParams(self, param):
        if self.params.get(param) == None:
            print('[error] unknown param')
        else:
            self.params[param] = True
    
    def config(self, design, tcl_file):
        tcl_path = util.getScriptPath(self.design)
        ret = 'place_design'
        if self.params['cadence_version'] == '19':
            ret = 'place_design'
        elif self.params['cadence_version'] == '15':
            ret = 'placeDesign'
        else:
            Exception("Invalid Cadence version!\n")
            
        for i in self.params:
            if self.params[i] == True:
                ret = ret + " -" + i
        
        tcl = open(os.path.join(tcl_path, tcl_file + ".tcl"), 'w', encoding = 'utf-8')
        tcl.writelines(ret)
        tcl.close()

        return ret


class DREAMPlace():
    
    def __init__(self, design):
        self.design = design
        self.params = collections.OrderedDict()
        self.params["lef_input"] = ["path/to/lef_input"]
        self.params["def_input"] = "path/to/def_input"
        self.params["result_dir"] = "path/to/result/dir"
        self.params["gpu"] = 1
        self.params["num_bins_x"] = 512
        self.params["num_bins_y"] = 512
        self.params["global_place_stages"] = [{
            "num_bins_x" : self.params["num_bins_x"],
            "num_bins_y" : self.params["num_bins_y"],
            "iteration" : 1000,
            "learning_rate" : 0.01,
            "wirelength" : "weighted_average",
            "optimizer" : "nesterov"
        }]
    
    def setParams(self, param, value):
        if self.params.get(param) != None:
            self.params[param] = value
        else:
            assert False, "Unknown param"
    
    def getObjHDL(self):
        obj_path = util.getObjPath(self.design)
        obj_hdl = os.path.join(obj_path, self.design.top_name + ".vh")
        return obj_hdl

    def getFpDEF(self):
        run_path = util.getRunPath(self.design)
        def_file = os.path.join(run_path, "%s_after_fp.def" % self.design.top_name)
        return def_file

    def config(self, design, json_file):
        
        json_path = util.getScriptPath(self.design)
        json_path = os.path.join(json_path, "%s_to_place.json" % self.design.top_name)

        self.params["lef_input"] = [self.design.lef_input]
        self.params["def_input"] = self.getFpDEF()
        self.params["result_dir"] = util.getRunPath(self.design)

        with open(json_path, "w", encoding='utf-8') as json_file:
            json.dump(self.params, json_file, indent=4)
        

