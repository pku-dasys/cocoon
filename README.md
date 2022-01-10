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

## Setup
- Clone this repo:
  ```shell
  git clone https://github.com/pku-dasys/cocoon.git
  ```
- If you are going to use DREAMPlace and yosys in your flow, pull git submodules in the root directory. Then solve their own dependencies.
  ```shell
  git submodule init
  git submodule update
  ```
  Or alternatively, pull all the submodules when cloning the repo.
  ```shell
  git clone --recursive https://github.com/pku-dasys/cocoon.git
  ```
- Build DREAMPlace (optional):
  ```shell
  cd ./thirdparty/DREAMPlace/
  mkdir build 
  cd build/ 
  cmake .. -DCMAKE_INSTALL_PREFIX=../install
  make 
  make install
  ```
- Build yosys (optional):
  ```shell
  cd ./thirdparty/yosys/
  mkdir build
  cd build/
  make -f ../Makefile
  ```

## Basic Usage
Once you have installed the previous required dependencies, you can run Cocoon from the command line using your customized configuration file in INI format. 

Three demo configurations `demo/config.sample1.ini`, `demo/config.sample2.ini`, `demo/config.sample3.ini` are provided, where your can find detailed description of user-defined options from the comments. Here's an example of 2 parallel flows.
```ini
[gcd]
# Design settings
design_name = gcd
is_Chisel_design = False
rtl_input = ./gcd/gcd.v
Chisel_input = 
result_dir = ../results/
clk_name = clk
delay = 1000

# Library settings
lib_name = gscl45nm
lef_input = ./lib/gscl45nm.lef
liberty_input = ./lib/gscl45nm.lib

# Flow settings
flow = {'synth':'yosys', 'placement':'dreamplace', 'routing':'innovus'}
n_iter_IFT = 0
verbose = False
cadence_version = 19


[ALU(Chisel)]
# Design settings
design_name = AluTop
is_Chisel_design = True
rtl_input = 
Chisel_input = ./alu-chisel/
result_dir = ../results/
clk_name = clk
delay = 1000

# Library settings
lib_name = gscl45nm
lef_input = ./lib/gscl45nm.lef
liberty_input = ./lib/gscl45nm.lib

# Flow settings
flow = {'synth':'genus', 'placement':'innovus', 'routing':'innovus'}
n_iter_IFT = 0
verbose = False
cadence_version = 19
```
You can directly run with the sample configurations with the demo designs, gcd (Verilog) and ALU (Chisel), together with the open-source FreePDK45nm library we provide in `./demo/`. For example:
```bash
cd cocoon/
python run.py ./demo/config.sample1.ini
```
With correctly customized configuration, you can run your own flow by executing:
```bash
cd cocoon/
python run.py /Path/to/your/config.ini
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
