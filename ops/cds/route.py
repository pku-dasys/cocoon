import sys
sys.path.append("../..")
import util

class InnovusRoute():
    def __init__(self, design):
        self.design = design
        self.params = dict()
        self.paramsPassive = dict()
        self.params['highFrequency'] = False
        self.params['viaPillarOpt'] = False

        self.paramsPassive['clockEco'] = False
        self.paramsPassive['trackOpt'] = False
        self.paramsPassive['idealClock'] = False
        self.paramsPassive['viaOpt'] = False
        self.paramsPassive['wireOpt'] = False

        self.paramsPassive['placementCheck'] = False
        self.paramsPassive['noPlacementCheck'] = False

        self.paramsPassive['globalDetail'] = False
        self.paramsPassive['detail'] = False

        self.params['passiveFill'] = False

    def setParams(self, param, optional):
        if self.params.get(param) is not None:
            self.params[param] = optional
        else:
            if self.paramsPassive.get(param) is not None:
                self.paramsPassive[param] = optional
            else:
                assert False, 'Unknown param'

    def config(self, design, tcl_file):
        tcl_path = util.getScriptPath(self.design, "Cadence")
        ret = 'routeDesign'
        for i in self.params:
            if self.params[i]:
                ret = ret + " -" + i

        assert not (self.paramsPassive['placementCheck'] and self.paramsPassive['noPlacementCheck']),\
            'Option -placementCheck and -noPlacementCheck are mutually exclusive.'
        assert not (self.paramsPassive['globalDetail'] and self.paramsPassive['detail']),\
            'Option -globalDetail and -detail are mutually exclusive.'

        if not self.params['passiveFill']:
            for i in self.paramsPassive:
                if self.paramsPassive[i]:
                    ret = ret + " -" + i

        tcl = open(tcl_path + "/" + tcl_file + ".tcl", 'w', encoding='utf-8')
        tcl.writelines(ret)
        tcl.close()

        return ret