import time
import os
import subprocess


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

    def Chisel2RTL(self, verbose):
        """
        Compile Chisel design to single verilog file
        """
        print("========== Compiling Chisel to Verilog... ==========")
        chisel_dir = self.Chisel_input
        output = "" if verbose else f" > {os.path.join(self.result_dir, self.top_name, self.lib_name, 'reports/', 'sbt.log')}"
        cmd = f'sbt "runMain {self.top_name}"' + output
        subprocess.run(cmd, cwd=chisel_dir, shell=True)
    
        self.rtl_input = os.path.join(self.Chisel_input, 'generated', '%s.v'%self.top_name)

