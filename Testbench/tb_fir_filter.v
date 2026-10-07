`timescale 1ns/1ps

module tb_fir_filter;
    initial begin
       $dumpfile("fir_waveform.vcd");
       $dumpvars(0, tb_fir_filter);
    end

    parameter NUM_TAPS = 121;

    reg clk;
    reg rst;
    reg valid_in;
    reg signed [15:0] sample_in;

    wire valid_out;
    wire signed [15:0] sample_out;

    // ------------------------------------------------
    // DUT
    // ------------------------------------------------

    fir_filter #(
        .NUM_TAPS(NUM_TAPS)
    ) dut (
        .clk(clk),
        .rst(rst),
        .valid_in(valid_in),
        .sample_in(sample_in),
        .valid_out(valid_out),
        .sample_out(sample_out)
    );

    // ------------------------------------------------
    // Clock: 100 MHz
    // ------------------------------------------------

    always #5 clk = ~clk;

    // ------------------------------------------------
    // Input ECG samples
    // ------------------------------------------------

    integer input_file;
    integer sample;
    integer result_file;

    integer count;

    // ------------------------------------------------
    // Test
    // ------------------------------------------------

    initial begin

        clk       = 1'b0;
        rst       = 1'b1;
        valid_in  = 1'b0;
        sample_in = 16'sd0;

        input_file = $fopen(
            "Data/ecg_noisy_fixed.txt",
            "r"
        );

        result_file = $fopen(
            "Data/ecg_filtered_verilog.txt",
            "w"
        );

        if (input_file == 0) begin
            $display("ERROR: Cannot open input file.");
            $finish;
        end

        if (result_file == 0) begin
            $display("ERROR: Cannot open output file.");
            $finish;
        end

        // Hold reset for two clock cycles
        #20;
        rst = 1'b0;

        count = 0;

        while (!$feof(input_file)) begin

            if ($fscanf(input_file, "%d\n", sample) == 1) begin

                @(negedge clk);

                sample_in = sample;
                valid_in  = 1'b1;

                @(negedge clk);

                valid_in = 1'b0;

                @(posedge clk);

                if (valid_out) begin
                    $fwrite(
                        result_file,
                        "%d\n",
                        sample_out
                    );

                    count = count + 1;
                end
            end

        end

        $fclose(input_file);
        $fclose(result_file);

        $display("----------------------------------------");
        $display("Simulation complete.");
        $display("Output samples: %0d", count);
        $display("----------------------------------------");

        #20;
        $finish;

    end

endmodule