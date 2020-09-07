from designcfg import Design
import engine
import subprocess, os

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
        #op_synth = "GenusSynth"
        #self.ops.append((op_synth, "to_synth"))

        op_synth = "YosysSynth"
        self.ops.append((op_synth, "to_synth")) 

        op_floorplan = "InnovusFloorplan"
        #self.ops.append((op_floorplan, "to_floorplan"))

        #self.params_fp.append(("r","1.0 0.7 0.0 0.0 0.0 0.0"))

        op_pdn = "InnovusPDN"
        #self.ops.append((op_pdn, "to_pdn"))

        op_place = "InnovusPlace"
        #self.ops.append((op_place, "to_place"))

        op_cts = "InnovusCTS"
        #self.ops.append((op_cts, "to_cts"))

        op_route = "InnovusRoute"
        #self.ops.append((op_route, "to_route"))

        op_drc = "InnovusDRC"
        #self.ops.append((op_drc, "to_drc"))


if __name__ == "__main__":

    design = Design("gcd")

    my_flow = MyFlow()
    my_flow.flow()

    res = engine.run(design, my_flow)

