module behav_counter(d, clk, clear, load, up_down, qd);

input   [7:0] d;
input   clk;
input   clear;
input   load;
input   up_down;
output  [7:0] qd;

reg     [7:0] cnt;

always @ (posedge clk)
begin
  if (!clear)
    cnt <= 8'h00;
  else if (load)
    cnt <= d;
  else if (up_down)
    cnt <= cnt + 1;
  else
    cnt <= cnt - 1;
end 

assign qd = cnt;

endmodule
