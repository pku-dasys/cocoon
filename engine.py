import subprocess
import os
import util
import ops.cds.syn as syn
import ops.cds.floorplan as fp
import ops.cds.pdn as pdn
import ops.cds.place as place
import ops.cds.cts as cts
import ops.cds.route as route
import ops.cds.drc as drc
import time


def run(design, flow):
    design_name = design.top_name
    run_path = util.getRunPath(design)
    # print(run_path)
    os.system("mkdir -p %s && rm -r %s*" % (run_path, run_path))
    make_file = open(os.path.join(run_path, "Makefile"), "w")
    
    tcl_path = util.getScriptPath(design)
    os.system("mkdir -p %s && rm -r %s*" % (tcl_path, tcl_path))
    overall_tcl = open(os.path.join(tcl_path, "flow.tcl"), 'w', encoding='utf-8')

    obj_path = util.getObjPath(design)
    os.system("mkdir -p %s && rm -r %s*" % (obj_path, obj_path))
    os.system(f"cp {design.rtl_input} {obj_path}")

    rpt_path = util.getRptPath(design)
    os.system("mkdir -p %s && rm -r %s*" % (rpt_path, rpt_path))

    for x in flow.ops:
        if x[0] == "GenusSynth":
            script_path = "../scripts/"
            tmp_op_syn = syn.GenusSynth(design)
            tmp_op_syn.config(design_name + "_" + x[1])
            make_file.write("all:\n")
            make_file.write("\tgenus -legacy_ui -batch -files " + script_path + design_name + "_" + x[1] + ".tcl\n")
        
        if x[0] == "yosys":
            script_path = "../scripts/"
            tmp_op_syn = syn.YosysSynth(design)
            tmp_op_syn.config(design_name + "_" + x[1], flow)
            make_file.write("all:\n")
            yosys_path = os.path.join(flow.yosys_bin_path, "yosys")
            save_log = f" | tee -a {os.path.join(rpt_path, 'yosys.log')}\n"
            make_file.write(f"\t{yosys_path} " + script_path + design_name + "_" + x[1] + ".ys" + save_log)

        if x[0] == "InnovusFloorplan":
            tmp_op_fp = fp.InnovusFloorplan(design)
            for key, val in flow.params_fp.items():
                tmp_op_fp.setParams(key, val)
            tmp_op_fp.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s%s_to_floorplan.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusPDN":
            tmp_op_pdn = pdn.InnovusPDN(design)
            tmp_op_pdn.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s%s_to_pdn.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusPlace":
            tmp_op_pdn = place.InnovusPlace(design)
            tmp_op_pdn.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s%s_to_place.tcl\n'%(tcl_path, design_name))
        
        if x[0] == "DREAMPlace":
            tmp_op_place = place.DREAMPlace(design)
            tmp_op_place.config(design, design_name + "_" + x[1])

        if x[0] == "InnovusCTS":
            tmp_op_cts = cts.InnovusCTS(design)
            tmp_op_cts.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s%s_to_cts.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusRoute":
            tmp_op_route = route.InnovusRoute(design)
            for key, val in flow.params_route.items():
                tmp_op_route.setParams(key, val)
            tmp_op_route.config(design, design_name + "_" + x[1])
               
            overall_tcl.write('source %s%s_to_route.tcl\n'%(tcl_path, design_name))
            # overall_tcl.write('set dbgLefDefOutVersion 5.8\ndefOut -floorplan -netlist -routing %s.def\n'%(design_name))	
        if x[0] == "InnovusDRC":
            tmp_op_drc = drc.InnovusDRC(design)
            tmp_op_drc.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s%s_to_drc.tcl\n'%(tcl_path, design_name))
    
    if flow.flow['placement'] == "innovus":
        make_file.write("\tinnovus -batch -files " + script_path + "flow.tcl")
    elif flow.flow['placement'] == "dreamplace":
        make_file.write("\tinnovus -batch -files " + script_path + "%s_to_floorplan.tcl\n" % design_name)
        save_log = f" | tee -a {os.path.join(rpt_path, 'dreamplace.log')}\n"
        make_file.write("\tpython %s %s" % (flow.dreamplace_bin_path, script_path + "%s_to_place.json" % design_name) + save_log)
        make_file.write("\tinnovus -batch -files " + script_path + "%s_to_route.tcl\n" % design_name)

    make_file.close()
    overall_tcl.close()

    run_path = util.getRunPath(design)
    print("Current working directory: %s" % run_path)
    proc_make = subprocess.Popen('make', cwd=run_path)  # Start a child process
    proc_make.wait()   # Wait until the process finishes
    assert proc_make.poll() == 0, "The flow failed and the process finished abnormally"
    print("The basic flow has finished successfully!")
    print(f"Design is saved to {run_path}{design.top_name}\n\n")

    # Iterative Feedback Tuning
    if flow.n_iter_IFT > 0:
        for i in range(flow.n_iter_IFT):
            print("========== Start of the IFT iteration %d ==========\n" % (i+1))

            rpt_path = tmp_op_syn.getRptTiming()
            critical_path = util.parseTimingRpt(rpt_path)
            tmp_op_syn = syn.GenusSynth(design, critical_path)
            tmp_op_syn.config(design_name + "_" + "to_synth")

            proc_make = subprocess.Popen('make', cwd=run_path)  # Start a child process
            proc_make.wait()   # Wait until the process finishes
            assert proc_make.poll() == 0, "The flow failed and the process finished abnormally"
            print(f"========== Finish IFT round [{i+1}] ==========\n\n")

    return 0

