import time

class Design(object):
    def __init__(self):
        self.top_name = "design" + time.strftime("%Y-%m-%d", time.localtime())
        self.is_Chisel_design = False
        self.rtl_input = " "
        self.Chisel_input = " "
        self.result_dir = "./design/"

        self.lib_name = "gscl45nm"
        self.lef_input = " "
        self.liberty_input = " "

        self.clk_name = "clk"
        self.delay = 100
