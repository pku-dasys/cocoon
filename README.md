# Cocoon: An Infrastructure for Integrated EDA
Cocoon is an open-source infrastructure for integrated EDA with interoperability and interactivity. It contains a set of cross-tool interfaces and plays the role of EDA agent that can help IC designers choose EDA point tools to assemble a legal design flow and to produce ICs with a higher quality of results (QoR). It can also help EDA researchers and tool developer research new design methodology and cross-stage optimization. Below are key features of Cocoon:
- Agile RTL-to-GDSII frontend and backend VLSI flow generation.
- Completely user-defined tech library, component EDA tool and design constraints.
- Multi-flow parallelism and automatic iterative circuit timing optimization.

## Cocoon Architecture
![avatar](image/arch.png)

## Dependency
 - Python3
 - Genus or [Yosys](https://github.com/YosysHQ/yosys)
 - Innovus
 - [DREAMPlace](https://github.com/limbo018/DREAMPlace) (optional)
 - JDK 8+ and sbt (optional)
 
## Basic Usage
Once you have installed the previous required dependencies, you can run Cocoon from the command line using your customized configuration file in INI format. 

A demo configuration `demo/config.sample.ini` is provided, where your can find detailed description of user-defined options from the comments. Here's an example of a single flow:
```ini
[flow_No.1]
# Design settings
design_name = your_design_topmodule_name
is_Chisel_design = True
rtl_input = /Path/to/verilog/file
Chisel_input = /Path/to/Chisel/project/
result_dir = /Path/to/result/dir/
clk_name = clk
delay = 1000

# Library settings
lib_name = your_lib_name
lef_input = /Path/to/library/foo.lef
liberty_input = /Path/to/library/bar.lib

# External toolkit settings
cadence_version = 19
dreamplace_bin_path = /Path/to/DREAMPlace/install/dreamplace/Placer.py
yosys_bin_path = /Path/to/yosys/build/

# Flow settings
flow = {'synth':'yosys', 'placement':'dreamplace', 'routing':'innovus'}
n_iter_IFT = 0
verbose = True
```
You can then run your design flow by executing:
```bash
cd cocoon/
python run.py /Path/to/your_config.ini
```
## Ongoing work
 - Integrate more EDA tools
 - Efficient resource scheduling
 - Legality check (LVS, DRC, etc.) and post-simulation (e.g. timing, power)
 - Support design-space search and optimization

## Related works
- Berkeley [Hammer](https://github.com/ucb-bar/hammer/)
- Stanford [mflowgen](https://github.com/mflowgen/mflowgen)
- [SiliconCompiler](https://github.com/siliconcompiler/siliconcompiler)
- [qflow](https://github.com/RTimothyEdwards/qflow)

## Publication

If you use cocoon in your research, please cite our WOSET'20 paper: ``Jiaxi Zhang, Tuo Dai, Zhengzheng Ma, Yibo Lin, Guojie Luo, "Cocoon: An Open Source Infrastructure for Integrated EDA with Interoperability and Interactivity", Workshop on Open-Source EDA Technology (WOSET), November 2020.``
```
@article{zhang-cocoon-woset2020,
  title   = "{Cocoon: An Open Source Infrastructure for Integrated EDA with Interoperability and Interactivity}",
  author  = {Jiaxi Zhang and Tuo Dai and Zhengzheng Ma and Yibo Lin and Guojie Luo}
  journal = {Workshop on Open-Source EDA Technology (WOSET)},
  month   = {Nov},
  year    = {2020},
}
```