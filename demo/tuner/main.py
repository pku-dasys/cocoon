import sys
sys.path.append("../../")
from hyperopt import hp, tpe, fmin, Trials
import engine
import util
from myflow import MyFlow
from designcfg import Design

space = {
    # syn
    "syn_effort": hp.choice("syn_x1", ["low", "medium", "high"]),
    "syn_inc": hp.choice("syn_x2", [True, False]),
    "syn_spa": hp.choice("syn_x3", [True, False]),
    # place
    "place_con": hp.choice("place_x1", [True, False]),
    "place_inc": hp.choice("place_x2", [True, False]),
    "place_nop": hp.choice("place_x3", [True, False]),
    # route
    "route_gd": hp.choice("route_x1", [True, False]),
    "route_detail": hp.choice("route_x2", [True, False]),
    "route_clock": hp.choice("route_x3", [True, False])
}

design = Design("cgra")

def optFunc(args):

    flow = MyFlow()
    flow.flow()
    flow.params_syn.append(("effort", args["syn_effort"]))
    flow.params_syn.append(("is_incremental", args["syn_inc"]))
    flow.params_syn.append(("spatial", args["syn_spa"]))

    flow.params_place.append(("concurrent_macros", args["place_con"]))
    flow.params_place.append(("incremental", args["place_inc"]))
    flow.params_place.append(("noPrePlaceOpt", args["place_nop"]))

    flow.params_route.append(("globalDetail", args["route_gd"]))
    flow.params_route.append(("detail", args["route_detail"]))
    flow.params_route.append(("clockEco", args["route_clock"]))

    ckpt = engine.run(design, flow)
    res = util.getResult(ckpt, "Timing", "Innovus")
    return res

def tuning():

    trials = Trials()
    best = fmin(
        optFunc,
        space=space,
        algo=tpe.suggest,
        max_evals=200,
        trials=trials
    )
    print(best)

if __name__ == "__main__":
    tuning()