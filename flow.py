import ops.syn as syn
from cfg import Design
import subprocess, os

class MyFlow(object):

	def __init__(self):
		self.points = []
		self.ops = []

	def excute(self, design):
		design_name = design.top_name
		make_file = open("Makefile", "w")
		self.ops[0].config(design_name + "_" + self.points[0])
		make_file.write("all:\n")
		make_file.write("\tgenus -legacy_ui -batch -files " + design_name + "_" + self.points[0] + ".tcl\n")



if __name__ == "__main__":

	design = Design("TopModuleWrapper")

	my_flow = MyFlow()
	op_synth = syn.GenusSynth(design)
	my_flow.ops.append(op_synth)
	my_flow.points.append("to_synth")

	my_flow.excute(design)

	cmd = 'make'

	subprocess.Popen(cmd)

