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

def getRptPath(design, baseflow):
    if baseflow == "Cadence":
        rpt_path = home_path + "/design/" + design.top_name + "/" + design.lib_name + "/reports"
    elif baseflow == "Openroad":
        rpt_path = "/OpenROAD-flow/flow" + design.top_name + "/" + design.lib_name + "/reports"
    return rpt_path

def getObjPath(design, baseflow):
    if baseflow == "Cadence":
        obj_path = home_path + "/design/" + design.top_name + "/" + design.lib_name + "/objects"
    elif baseflow == "Openroad":
        obj_path = "/OpenROAD-flow/flow" + design.top_name + "/" + design.lib_name + "/objects"
    return obj_path

def getScriptPath(design, baseflow):
    if baseflow == "Cadence":
        script_path = home_path + "/design/" + design.top_name + "/" + design.lib_name + "/scripts"
    elif baseflow == "Openroad":
        script_path = "/OpenROAD-flow/flow" + design.top_name + "/" + design.lib_name + "/scripts"
    return script_path

def getRunPath(design, baseflow):
    if baseflow == "Cadence":
        run_path = home_path + "/design/" + design.top_name + "/" + design.lib_name + "/run"
    elif baseflow == "Openroad":
        run_path = "/OpenROAD-flow/flow" + design.top_name + "/" + design.lib_name + "/run"
    return run_path