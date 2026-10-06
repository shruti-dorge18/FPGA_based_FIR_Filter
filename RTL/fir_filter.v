module fir_filter #(
    parameter NUM_TAPS = 121
)(
    input  wire               clk,
    input  wire               rst,
    input  wire               valid_in,
    input  wire signed [15:0] sample_in,

    output reg                valid_out,
    output reg  signed [15:0] sample_out
);

    // ------------------------------------------------
    // Delay line
    // ------------------------------------------------

    reg signed [15:0] delay_line [0:NUM_TAPS-1];

    // ------------------------------------------------
    // Q1.15 FIR coefficients
    // ------------------------------------------------

    reg signed [15:0] coefficients [0:NUM_TAPS-1];

    initial begin
        $readmemh(
            "Coefficients/fir_coefficients_q15.hex",
            coefficients
        );
    end

    // ------------------------------------------------
    // FIR accumulator
    //
    // 16-bit sample × 16-bit coefficient
    //              ↓
    //          32-bit product
    //              ↓
    //       121 accumulated terms
    //              ↓
    //          Q2.30 result
    // ------------------------------------------------

    reg signed [47:0] accumulator;
    reg signed [47:0] scaled_output;

    integer i;

    // ------------------------------------------------
    // FIR operation
    // ------------------------------------------------

    always @(posedge clk) begin

        if (rst) begin

            for (i = 0; i < NUM_TAPS; i = i + 1)
                delay_line[i] <= 16'sd0;

            sample_out <= 16'sd0;
            valid_out  <= 1'b0;

        end

        else begin

            valid_out <= 1'b0;

            if (valid_in) begin

                // ------------------------------------
                // Shift delay line
                // ------------------------------------

                for (i = NUM_TAPS-1; i > 0; i = i - 1)
                    delay_line[i] <= delay_line[i-1];

                delay_line[0] <= sample_in;

                               // ------------------------------------
                // FIR accumulation
                //
                // Current input = x[n]
                // delay_line[0] = x[n-1]
                // delay_line[1] = x[n-2]
                // ...
                // ------------------------------------

                accumulator = 48'sd0;

                accumulator =
                    accumulator +
                    ($signed(sample_in) *
                     $signed(coefficients[0]));

                for (i = 0; i < NUM_TAPS-1; i = i + 1)
                    accumulator =
                        accumulator +
                        ($signed(delay_line[i]) *
                         $signed(coefficients[i+1]));

                // ------------------------------------
                // Q2.30 -> Q1.15
                // ------------------------------------

                scaled_output = accumulator >>> 15;

                // ------------------------------------
                // Saturation
                // ------------------------------------

                if (scaled_output > 32767)
                    sample_out <= 16'sh7FFF;

                else if (scaled_output < -32768)
                    sample_out <= 16'sh8000;

                else
                    sample_out <= scaled_output[15:0];

                valid_out <= 1'b1;
            end
        end
    end

endmodule