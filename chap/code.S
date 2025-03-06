r0:SubLUT, r2:MatRow, r4:k, r6:Result

lbu r1, r2, r4 ;MatRow[k]
lsl r1, r1, 2 ;4*MatRow[k]
lw r3, r0, r1 ;SubLUT[Vector[j]&0xF][MatRow[k]]
lsl r5, r4, 2 ;k*=4
lw r7, r6, r5 ;Result[k]
add r7, r7, r3 ;Result[k]+=SubLUT[Vector[j]&0xF][MatRow[k]]
sw r6, r5, r7 ;

;lfma add_reg: reg, base_reg: reg, offset: imm, ele_width: imm
lbu r1, r2, r4 ;MatRow[k]
lwo r7, r6, r4, 4
lfma r7, r0, r1, 4
sw r6, r5, r7 ;

;lfma result_reg: reg, add_base_reg: reg, add_offset: imm, lut_base_reg: reg, lut_offset: imm, ele_width: imm
lbu r1, r2, r4 ;MatRow[k]
lfma r7, r6, r4, r0, r1, 4
sw r6, r5, r7 ;

;lwms res_reg: reg, base_reg: reg, offset: imm, ele_width: imm
lbu r1, r2, r4 ;MatRow[k]
lwms r3, r0, r1, 2
lwms r7, r6, r4, 2

add r7, r7, r3 ;Result[k]+=SubLUT[Vector[j]&0xF][MatRow[k]]
sw r6, r5, r7 ;

lfma result_reg: reg, add_base_reg: reg, add_off: imm, lut_base_reg: reg, lut_off: imm, ele_width: imm
{
    add_addr = add_base_reg+add_offset*ele_width;
    lut_addr = lut_base_reg+lut_offset*ele_width;
    result_reg += [add_addr]+[lut_addr];
}

lwms res_reg: reg, base_reg: reg, offset: imm, ele_width: imm
{
    res_reg = [base_reg+offset*ele_width]
}