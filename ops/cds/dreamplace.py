import sys
import json
import collections
import util

class DREAMPlace():
    
    def __init__(self, design):
        self.design = design
        self.params = collections.OrderedDict()
        self.params["lef_input"] = ["path/to/lef_input"]
        self.params["def_input"] = "path/to/def_input"
        # self.params["verilog_input"] = "path/to/verilog_input"
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
        obj_path = util.getObjPath(self.design, "Cadence")
        obj_hdl = obj_path + "/" + self.design.top_name + ".vh"
        return obj_hdl

    def getLEF(self):
        lef_path = util.getLefPath(self.design, "Cadence")
        lef_file = lef_path + "/" + util.getLef(self.design)
        return lef_file

    def getFpDEF(self):
        run_path = util.getRunPath(self.design, "Cadence")
        def_file = run_path + "/%s_after_fp.def" % self.design.top_name
        return def_file

    def config(self, design, json_file):
        
        json_path = util.getScriptPath(self.design, "Cadence")
        json_path += "/%s_to_place.json" % self.design.top_name

        self.params["lef_input"] = [self.getLEF()]
        self.params["def_input"] = self.getFpDEF()
        # self.params["verilog_input"] = self.getObjHDL()
        self.params["result_dir"] = util.getRunPath(self.design, "Cadence")

        with open(json_path, "w", encoding='utf-8') as json_file:
            json.dump(self.params, json_file, indent=4)
        





