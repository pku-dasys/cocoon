# ####################################################################

#  Created by Genus(TM) Synthesis Solution 19.12-s121_1 on Mon Aug 10 11:16:47 CST 2020

# ####################################################################

set sdc_version 2.0

set_units -capacitance 1000fF
set_units -time 1000ps

# Set the current design
current_design gcd

create_clock -name "clk" -period 0.1 -waveform {0.0 0.05} [get_ports clk]
set_clock_transition 0.4 [get_clocks clk]
set_clock_gating_check -setup 0.0 
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports resp_rdy]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports reset]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports req_val]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[0]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[1]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[2]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[3]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[4]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[5]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[6]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[7]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[8]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[9]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[10]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[11]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[12]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[13]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[14]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[15]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[16]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[17]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[18]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[19]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[20]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[21]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[22]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[23]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[24]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[25]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[26]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[27]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[28]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[29]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[30]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {req_msg[31]}]
set_input_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports clk]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports resp_val]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[0]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[1]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[2]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[3]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[4]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[5]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[6]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[7]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[8]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[9]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[10]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[11]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[12]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[13]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[14]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports {resp_msg[15]}]
set_output_delay -clock [get_clocks clk] -add_delay 0.0 [get_ports req_rdy]
set_wire_load_mode "enclosed"
