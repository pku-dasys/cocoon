# Cocoon: An Infrastructure for Integrated EDA
Cocoon is an open-source infrastructure for integrated EDA with interoperability and interactivity.
It contains a set of cross-tool interfaces and plays the role of EDA agent that can help IC designers 
choose EDA point tools to assemble a legal design flow and to produce ICs with a higher quality of results (QoR).
It can also help EDA researchers and tool developer research new design methodology and cross-stage optimization.

## Cocoon Architecture
![avatar](image/arch.png)

## Dependency
 - python3
 - [Yosys](https://github.com/YosysHQ/yosys)
 - [Hpyeropt](https://github.com/hyperopt/hyperopt) (optional for tuning)
 - genus (optional)
 - innovus (optional)
 
## Demo
 1. Branch Flow
 	- `cd demo/branch/ && python3 flow.py`
 2. Flow Tuning
 	- `cd demo/tuner/ && python3 main.py`
 
## Ongoing work
 - Integrating other open source binaries
 - Legality Check
 - More demo flows
 - Beautify the UI

## Related works
- Berkeley [Hammer](https://github.com/ucb-bar/hammer/)
- Stanford [mflowgen](https://github.com/mflowgen/mflowgen)

## Publication

If you use cocoon in your research, please cite our WOSET'20 paper:
```
@article{zhang-cocoon-woset2020,
  title   = "{Cocoon: An Open Source Infrastructure for Integrated EDA with Interoperability and Interactivity}",
  author  = {Jiaxi Zhang and Tuo Dai and Zhengzheng Ma and Yibo Lin and Guojie Luo}
  journal = {Workshop on Open-Source EDA Technology (WOSET)},
  month   = {Nov},
  year    = {2020},
}
```
