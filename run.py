import engine
import sys
import util
from config import Config


if __name__ == "__main__":

    if (len(sys.argv) != 2):
        print("ERROR: Invalid command line arguments")
        print("Usage: python flow.py /path/to/your/config")
        exit(1)
    
    util.printWelcome()
    config_file = sys.argv[1]
    config = Config(config_file)

    flows = config.parse()

    # Under construction (Multi-task)
    for flow in flows:
        engine.run(flow[0], flow[1])