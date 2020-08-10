import subprocess
import util
import ops.cds.syn as syn1
import ops.openroad.syn as syn2

def run(design, flow):
    design_name = design.top_name
    for x in flow.ops:
        if x[0] == "GenusSynth":
            run_path = util.getRunPath(design, "Cadence")
            make_file = open("Makefile", "w")
            tmpop = eval("syn1." + "GenusSynth" + "(design)")
            tmpop.config(design, design_name + "_" + x[1])
            make_file.write("all:\n")
            make_file.write("\tgenus -legacy_ui -batch -files " + design_name + "_" + x[1] + ".tcl\n")
        #if x[0] == "OpenROADSynth":

    #cmd = 'make'
    #subprocess.Popen(cmd)

    return 0

