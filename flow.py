from designcfg import Design
import engine
import subprocess, os

#define a customized flow
class MyFlow(object):

    def __init__(self):
        self.ops = []

    def flow(self):
        op_synth = "GenusSynth"
        self.ops.append((op_synth, "to_synth"))


if __name__ == "__main__":

    design = Design("gcd")

    my_flow = MyFlow()
    flow = my_flow.flow()

    res = engine.run(design, my_flow)

