
class Design(object):
    def __init__(self, top_name):
        self.top_name = top_name
        self.rtl_file = "{TopModuleWrapper.v}"
        self.hdl_path = "./design/cgra/hdl"
        self.lib_path = "./design/lib"
        self.mmmc_file = "{./flow.view}"
        self.lef_file = self.lib_path + "/gscl45nm.lef"
        self.lib_file = "gscl45nm.lib"
        self.clk_name = "clk"
        self.delay = 10000
        self.rpt_path = "./design/cgra/report"
        self.obj_path = "./design/cgra/object"
        self.script_path = "./design/cgra/scripts"

