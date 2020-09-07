import sys
sys.path.append("../../")
from designcfg import Design
import engine
import subprocess, os
import util
util.home_path = util.home_path + "/../.."

#define a customized flow
class MyFlow(object):

    def __init__(self):
        self.ops = []
        self.params_syn = []
        self.params_fp = []
        self.params_pdn = []
        self.params_place = []
        self.params_cts = []
        self.params_route = []
        self.params_drc = []

    def flow(self):

        op_synth = []
        op_synth.append(("YosysSynth", "to_synth", "Timing"))
        op_synth.append(("GenusSynth", "to_synth", "Timing"))
        self.ops.append(op_synth)

        op_floorplan = [("InnovusFloorplan", "to_floorplan")]
        self.ops.append(op_floorplan)
        self.params_fp.append(("r","1.0 0.7 0.0 0.0 0.0 0.0"))

        op_pdn = ["InnovusPDN", "to_pdn"]
        self.ops.append(op_pdn)

        op_place = ["InnovusPlace", "to_place"]
        self.ops.append(op_place)

        op_cts = ["InnovusCTS", "to_cts"]
        self.ops.append(op_cts)

        op_route = ["InnovusRoute", "to_route"]
        self.ops.append(op_route)



if __name__ == "__main__":

    design = Design("gcd")

    my_flow = MyFlow()
    my_flow.flow()

    res = engine.run(design, my_flow)


   

    


    

