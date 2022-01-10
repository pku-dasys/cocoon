import configparser
from flow import MyFlow
from designcfg import Design
import os


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
        self.cocoon_home = os.getcwd()
        self.config_dir = os.path.dirname(os.path.abspath(config_file))
    
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
        if not os.path.isabs(design.rtl_input):  # Relative path
            design.rtl_input = os.path.join(self.config_dir, design.rtl_input)

        design.Chisel_input = sec.get('Chisel_input')
        if not os.path.isabs(design.Chisel_input):  # Relative path
            design.Chisel_input = os.path.join(self.config_dir, design.Chisel_input)

        design.result_dir = sec.get('result_dir')
        if not os.path.isabs(design.result_dir):  # Relative path
            design.result_dir = os.path.join(self.config_dir, design.result_dir)

        design.lef_input = sec.get('lef_input')
        if not os.path.isabs(design.lef_input):  # Relative path
            design.lef_input = os.path.join(self.config_dir, design.lef_input)

        design.liberty_input = sec.get('liberty_input')
        if not os.path.isabs(design.liberty_input):  # Relative path
            design.liberty_input = os.path.join(self.config_dir, design.liberty_input)

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

        if sec.get('cadence_version'):
            flow.cadence_version = sec.get('cadence_version')

        flow.yosys_bin_path = os.path.join(self.cocoon_home, 'thirdparty/yosys/build/')
        flow.dreamplace_bin_path = os.path.join(self.cocoon_home, 'thirdparty/DREAMPlace/install/dreamplace/Placer.py')

        flow.config()
        return flow


        


        
