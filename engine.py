import subprocess
import os
import util
import ops.cds.syn as syn1
import ops.cds.floorplan as fp1
import ops.cds.pdn as pdn1
import ops.cds.place as place1
import ops.cds.dreamplace as dreamplace
import ops.cds.cts as cts1
import ops.cds.route as route1
import ops.cds.drc as drc1
# import ops.openroad.syn as syn2
import time


def run(design, flow):
    design_name = design.top_name
    run_path = util.getRunPath(design, "Cadence")
    # print(run_path)
    os.system("mkdir -p %s && rm -r %s/*" % (run_path, run_path))
    make_file = open(run_path + "/" + "Makefile", "w")
    tcl_path = util.getScriptPath(design, "Cadence")
    os.system("mkdir -p %s && rm -r %s/*" % (tcl_path, tcl_path))
    overall_tcl = open(tcl_path + "/" + "flow.tcl", 'w', encoding='utf-8')
    for x in flow.ops:
        if x[0] == "GenusSynth":
            script_path = "../scripts/"
            tmp_op_syn = eval("syn1." + "GenusSynth" + "(design)")
            tmp_op_syn.config(design, design_name + "_" + x[1])
            make_file.write("all:\n")
            make_file.write("\tgenus -legacy_ui -batch -files " + script_path + design_name + "_" + x[1] + ".tcl\n")

        if x[0] == "InnovusFloorplan":
            tmp_op_fp = eval("fp1." + "InnovusFloorplan" + "(design)")
            for key, val in flow.params_fp.items():
                tmp_op_fp.setParams(key, val)
            tmp_op_fp.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_floorplan.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusPDN":
            tmp_op_pdn = eval("pdn1." + "InnovusPDN" + "(design)")
            tmp_op_pdn.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_pdn.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusPlace":
            tmp_op_pdn = eval("place1." + "InnovusPlace" + "(design)")
            tmp_op_pdn.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_place.tcl\n'%(tcl_path, design_name))
        
        if x[0] == "DREAMPlace":
            tmp_op_place = dreamplace.DREAMPlace(design)
            tmp_op_place.config(design, design_name + "_" + x[1])

        if x[0] == "InnovusCTS":
            tmp_op_cts = eval("cts1." + "InnovusCTS" + "(design)")
            tmp_op_cts.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_cts.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusRoute":
            tmp_op_route = eval("route1." + "InnovusRoute" + "(design)")
            for key, val in flow.params_route.items():
                tmp_op_route.setParams(key, val)
            tmp_op_route.config(design, design_name + "_" + x[1])
               
            overall_tcl.write('source %s/%s_to_route.tcl\n'%(tcl_path, design_name))
            # overall_tcl.write('set dbgLefDefOutVersion 5.8\ndefOut -floorplan -netlist -routing %s.def\n'%(design_name))	
        if x[0] == "InnovusDRC":
            tmp_op_drc = eval("drc1." + "InnovusDRC" + "(design)")
            tmp_op_drc.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_drc.tcl\n'%(tcl_path, design_name))
    
    if flow.flow_type == "innovus":
        make_file.write("\tinnovus -batch -files " + script_path + "flow.tcl")
    else:  # DREAMPlace flow
        make_file.write("\tinnovus -batch -files " + script_path + "%s_to_floorplan.tcl\n" % design_name)
        make_file.write("\tpython %s %s\n" % (flow.dreamplace_path, script_path + "%s_to_place.json" % design_name))
        make_file.write("\tinnovus -batch -files " + script_path + "%s_to_route.tcl\n" % design_name)

    make_file.close()
    overall_tcl.close()

    run_path = util.getRunPath(design, "Cadence")
    print("Current Path: %s" % run_path)
    proc_make = subprocess.Popen('make', cwd=run_path)  # Start a child process
    proc_make.wait()   # Wait until the process finishes
    assert proc_make.poll() == 0, "The flow failed and the process finished abnormally"
    print("The basic flow has finished successfully!")

    # Iterative Feedback Tuning
    if flow.n_iter_IFT > 0:
        for i in range(flow.n_iter_IFT):
            print("Start of the IFT iteration %d" % (i+1))

            rpt_path = tmp_op_syn.getRptTiming()
            critical_path = util.parseTimingRpt(rpt_path)
            tmp_op_syn = syn1.GenusSynth(design, critical_path)
            tmp_op_syn.config(design, design_name + "_" + "to_synth")

            proc_make = subprocess.Popen('make', cwd=run_path)  # Start a child process
            proc_make.wait()   # Wait until the process finishes
            assert proc_make.poll() == 0, "The flow failed and the process finished abnormally"

    return 0

