from multiprocessing import Process
import time
import engine
import sys
import util
from config import Config


if __name__ == "__main__":

    if (len(sys.argv) != 2):
        print("ERROR: Invalid command line arguments")
        print("Usage: python run.py /path/to/your/config")
        exit(1)
    
    begin_t = time.time()
    util.printWelcome()
    config_file = sys.argv[1]
    config = Config(config_file)

    flows = config.parse()
    procs = []

    for flow in flows:
        procs.append(Process(target=engine.run, args=(flow[0], flow[1], flow[2],)))
    
    for p in procs:
        p.start()

    for p in procs:
        p.join()
    
    end_t = time.time()
    print("=============== Cocoon finishes {} flow(s) in {:.1f} seconds ===============\n\n".format(len(flows), end_t - begin_t))