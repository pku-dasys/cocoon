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
        hdl_path = home_path + "/data/" + design.top_name + "/hdl"
    elif baseflow == "Yosys":
        hdl_path = home_path + "/data/" + design.top_name + "/hdl"
    return hdl_path

def getLibPath(design, baseflow):
    if baseflow == "Cadence":
        lib_path = home_path + "/data/lib"
    elif baseflow == "Yosys":
        lib_path = home_path + "/data/lib"
    return lib_path

def getLefPath(design, baseflow):
    if baseflow == "Cadence":
        lef_path = home_path + "/data/lib"
    elif baseflow == "Yosys":
        lef_path = ""
    return lef_path

def getRptPath(design, baseflow):
    if baseflow == "Cadence":
        rpt_path = home_path + "/data/" + design.top_name + "/" + design.lib_name + "/reports"
    elif baseflow == "Yosys":
        rpt_path = home_path + "/data/" + design.top_name + "/" + design.lib_name + "/reports"
    return rpt_path

def getObjPath(design, baseflow):
    if baseflow == "Cadence":
        obj_path = home_path + "/data/" + design.top_name + "/" + design.lib_name + "/objects"
    elif baseflow == "Yosys":
        obj_path = home_path + "/data/" + design.top_name + "/" + design.lib_name + "/objects"
    return obj_path

def getScriptPath(design, baseflow):
    if baseflow == "Cadence":
        script_path = home_path + "/data/" + design.top_name + "/" + design.lib_name + "/scripts"
    elif baseflow == "Yosys":
        script_path = home_path + "/data/" + design.top_name + "/" + design.lib_name + "/scripts"
    return script_path

def getRunPath(design, baseflow):
    if baseflow == "Cadence":
        run_path = home_path + "/data/" + design.top_name + "/" + design.lib_name + "/run"
    elif baseflow == "Yosys":
        run_path = home_path + "/data/" + design.top_name + "/" + design.lib_name + "/run"
    return run_path

def getResult(design, optFunc, baseFlow):
    if optFunc == "Timing":
        rpt = getRptPath(design, baseFlow)
        res = rpt + "/timing.rpt"
    return res

def evaluate(ckpt_list, optFunc, baseFlow):
    idx = None
    res = 1000000
    for ckpt in ckpt_list:
        tmp = getResult(ckpt, optFunc, baseFlow)
        if tmp < res:
            res = tmp
            idx = ckpt
    return idx

def getCheckpoint(file_path):
    # read checkpoint from path
    return file_path
    

def saveCheckpoint(ckpt, file_path):
    # save checkpoint to path
    pass

