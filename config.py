import configparser
from flow import MyFlow
from designcfg import Design


class Config:
    """
    Parse the config file
        Input: config file
        Output: (list)[(Design1, MyFlow1), ..., (Designx, MyFlowx)]
    """
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        try:
            self.config.read(config_file)
        except:
            print("Error: Fail to read config file %s" % config_file)
        # List of different sections (flows) of the .ini file
        self.multi_flows = self.config.sections()
    
    def parse(self):
        flows = []
        for flow_name in self.multi_flows:
            flows.append((self.createDesign(flow_name), self.createFlow(flow_name), flow_name))
        return flows

    def createDesign(self, sec_name):
        design = Design()
        sec = self.config[sec_name]
        design.top_name = sec.get('design_name')

        assert sec.get('lib_name'), "Argument lib_name is required!\n"
        design.lib_name = sec.get('lib_name')

        design.is_Chisel_design = sec.getboolean('is_Chisel_design')
        design.rtl_input = sec.get('rtl_input')
        design.Chisel_input = sec.get('Chisel_input')
        design.result_dir = sec.get('result_dir')
        design.lef_input = sec.get('lef_input')
        design.liberty_input = sec.get('liberty_input')
        design.clk_name = sec.get('clk_name')
        design.delay = sec.getint('delay')

        if design.is_Chisel_design:
            verbose = sec.getboolean('verbose')
            design.Chisel2RTL(verbose)

        return design

    def createFlow(self, sec_name):
        flow = MyFlow()
        sec = self.config[sec_name]

        assert sec.get('flow'), "Argument flow is required!\n"
        flow.flow = eval(sec.get('flow'))

        assert sec.get('n_iter_IFT'), "Argument n_iter_IFT is required!\n"
        flow.n_iter_IFT = sec.getint('n_iter_IFT')

        assert not ((flow.flow['synth'] == 'yosys') and (flow.n_iter_IFT > 0)), "IFT cannot work with Yosys, try GenusSynth instead.\n"

        flow.verbose = sec.getboolean('verbose')

        if sec.get('dreamplace_bin_path'):
            flow.dreamplace_bin_path = sec.get('dreamplace_bin_path')
        if sec.get('yosys_bin_path'):
            flow.yosys_bin_path = sec.get('yosys_bin_path')
        if sec.get('cadence_version'):
            flow.cadence_version = sec.get('cadence_version')

        flow.config()
        return flow


        


        
