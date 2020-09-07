set hdl_files {gcd.v}
set DESIGN gcd
set clkpin clk
set delay 100
set_attribute hdl_search_path /Users/daitoto/Desktop/code/DASYS/cocoon/demo/tuner/../../data/gcd/hdl
set_attribute lib_search_path /Users/daitoto/Desktop/code/DASYS/cocoon/demo/tuner/../../data/lib
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
synthesize -to_mapped -effort -is_incremental
report timing > /Users/daitoto/Desktop/code/DASYS/cocoon/demo/tuner/../../data/gcd/gscl45nm/reports/timing_synth.rpt
report gates  > /Users/daitoto/Desktop/code/DASYS/cocoon/demo/tuner/../../data/gcd/gscl45nm/reports/gates_synth.rpt
report power  > /Users/daitoto/Desktop/code/DASYS/cocoon/demo/tuner/../../data/gcd/gscl45nm/reports/gates_synth.rpt
write_hdl -mapped >  /Users/daitoto/Desktop/code/DASYS/cocoon/demo/tuner/../../data/gcd/gscl45nm/objects/gcd.vh
write_sdc >  /Users/daitoto/Desktop/code/DASYS/cocoon/demo/tuner/../../data/gcd/gscl45nm/objects/gcd.sdc
