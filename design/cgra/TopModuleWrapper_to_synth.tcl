set hdl_files {TopModuleWrapper.v}
set DESIGN TopModuleWrapper
set clkpin clk
set delay 10000
set_attribute hdl_search_path ./design/cgra/hdl
set_attribute lib_search_path ./design/lib
set_attribute information_level 6 
set_attribute library gscl45nm.lib
read_hdl ${hdl_files} 
elaborate $DESIGN 
set clock [define_clock -period ${delay} -name ${clkpin} [clock_ports]]
external_delay -input   0 -clock clk [find / -port ports_in/*]
external_delay -output  0 -clock clk [find / -port ports_out/*]
dc::set_clock_transition .4 clk
check_design -unresolved
report timing -lint
synthesize -effort -is_incremental
report timing > ./design/cgra/report/timing_synth.rpt
report gates  > ./design/cgra/report/gates_synth.rpt
report power  > ./design/cgra/report/power_synth.rpt
write_hdl -mapped >  ./design/cgra/object/TopModuleWrapper.vh
write_sdc >  ./design/cgra/object/TopModuleWrapper_synth.sdc
