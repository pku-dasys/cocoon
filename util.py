import os

home_path = os.getcwd()
#print(home_path)

def getHDL(design):
    return design.rtl_file

def getLib(design):
    return design.lib_file

def getLef(design):
    return design.lef_file

def getMmmc(design):
    return design.mmmc_file


def getHDLPath(design, baseflow):
    if baseflow == "Cadence":
        hdl_path = home_path + "/design/" + design.top_name + "/hdl"
    elif baseflow == "Openroad":
        hdl_path = "/OpenROAD-flow/flow/designs/design/" + design.top_name + "/hdl"
    return hdl_path

def getLibPath(design, baseflow):
    if baseflow == "Cadence":
        lib_path = home_path + "/design/lib"
    elif baseflow == "Openroad":
        lib_path = "/OpenROAD-flow/flow/platforms/" + design.lib_name
    return lib_path

def getLefPath(design, baseflow):
    if baseflow == "Cadence":
        lef_path = home_path + "/design/lib"
    elif baseflow == "Openroad":
        lef_path = ""
    return lef_path

def getRptPath(design):
    """
    get the reports directory
    """
    return os.path.join(design.result_dir, design.top_name, design.lib_name, "reports/")

def getObjPath(design):
    """
    get the objects directory
    """
    return os.path.join(design.result_dir, design.top_name, design.lib_name, "objects/")

def getScriptPath(design):
    """
    get the scripts directory
    """
    return os.path.join(design.result_dir, design.top_name, design.lib_name, "scripts/")

def getRunPath(design):
    """
    get the working directory
    """
    return os.path.join(design.result_dir, design.top_name, design.lib_name, "run/")

def createMMMC(design, path):
    """
    Create a mmmc file according to the design
    """
    mmmc = open(path, mode='w')
    mmmc.write("create_library_set -name %s -timing {%s}\n" % (design.lib_name, design.liberty_input))
    mmmc.write("create_rc_corner -name default_rc_corner -preRoute_res {1.0} -preRoute_cap {1.0} -preRoute_clkres {0.0} -preRoute_clkcap {0.0} -postRoute_res {1.0} -postRoute_cap {1.0} -postRoute_xcap {1.0} -postRoute_clkres {0.0} -postRoute_clkcap {0.0}\n")
    mmmc.write("create_delay_corner -name default_delay_corner -library_set {%s} -rc_corner {default_rc_corner}\n" % design.lib_name)
    mmmc.write("create_constraint_mode -name common -sdc_files {%s}\n" % os.path.join(getObjPath(design), design.top_name + ".sdc"))
    mmmc.write("create_analysis_view -name default_view_hold -constraint_mode {common} -delay_corner {default_delay_corner}\n")
    mmmc.write("create_analysis_view -name default_view_setup -constraint_mode {common} -delay_corner {default_delay_corner}\n")
    mmmc.write("set_analysis_view -setup {default_view_setup} -hold {default_view_hold}\n")
    mmmc.close()
    
def parseTimingRpt(timing_rpt_path):
    """
    Args:
    timing_rpt_path: path/to/timing_synth.rpt
    Return:
    critical path in form (start-point, end-point)
    """
    timing_rpt = open(timing_rpt_path, mode='r')
    lines = timing_rpt.readlines()
    lines.reverse()
    start, end = None, None
    for line in lines:
        line = line.strip()
        if "End-point" in line:
            fields = line.split()
            end = fields[-1]
        elif "Start-point" in line:
            fields = line.split()
            start = fields[-1]
            break
    timing_rpt.close()
    
    return (start, end)

def printWelcome():

    content = """\
=======================================================
                       Cocoon
        - An Infrastructure for Integrated EDA -
                    by PKU-DASYS
======================================================="""

    print(content)