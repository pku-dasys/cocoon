from designcfg import Design
import engine
import subprocess, os

#define a customized flow
class MyFlow(object):

    def __init__(self):
        self.flow_type = ' '
        self.ops = []
        self.params_syn = {}
        self.params_fp = {"r" : None, "def_out": False}
        self.params_pdn = []
        self.params_place = {"def_out" : False}
        self.params_cts = []
        self.params_route = {"def_in" : False, "def_out" : True, "detailed_place" : False}
        self.params_drc = []
        self.n_iter_IFT = 0
        self.dreamplace_path = "/home/wxm/cocoon/extern_toolkits/DREAMPlace/install/dreamplace/Placer.py"

    def flow(self):
        self.flow_type = 'innovus'
        op_synth = "GenusSynth"
        self.ops.append((op_synth, "to_synth"))

        op_floorplan = "InnovusFloorplan"
        self.ops.append((op_floorplan, "to_floorplan"))
        self.params_fp["r"] = "1.0 0.7 0.0 0.0 0.0 0.0"
        self.params_fp["def_out"] = False

        op_pdn = "InnovusPDN"
        self.ops.append((op_pdn, "to_pdn"))

        op_place = "InnovusPlace"
        self.ops.append((op_place, "to_place"))
        self.params_place["def_out"] = False

        op_cts = "InnovusCTS"
        self.ops.append((op_cts, "to_cts"))

        op_route = "InnovusRoute"
        self.ops.append((op_route, "to_route"))
        self.params_route["def_in"] = False
        self.params_route["def_out"] = True
        self.params_route["detailed_place"] = False

        # op_drc = "InnovusDRC"
        #self.ops.append((op_drc, "to_drc"))
    
    def flow_dp(self):
        self.flow_type = 'dp'
        op_synth = "GenusSynth"
        self.ops.append((op_synth, "to_synth"))

        op_floorplan = "InnovusFloorplan"
        self.ops.append((op_floorplan, "to_floorplan"))
        self.params_fp["r"] = "1.0 0.7 0.0 0.0 0.0 0.0"
        self.params_fp["def_out"] = True

        op_place = "DREAMPlace"
        self.ops.append((op_place, "to_place"))
        self.params_place["def_out"] = True

        op_route = "InnovusRoute"
        self.ops.append((op_route, "to_route"))
        self.params_route["def_in"] = True
        self.params_route["def_out"] = True
        self.params_route["detailed_place"] = True


if __name__ == "__main__":

    design = Design("gcd")

    my_flow = MyFlow()
    my_flow.flow_dp()

    res = engine.run(design, my_flow)

