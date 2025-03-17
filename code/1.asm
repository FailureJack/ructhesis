;Result[k]+=SubLUT[Vector[j]&0xF][MatRow[k]]
;Result:r0, k:r2, SubLUT[Vector[j]&0xF]:r4, MatRow:r6

;MatRow
add r1, r6, r2
lbu r1, r1, 0
;SubLUT
lsl_add r3, r4, r1, 2
lw r3, r3, 0
;Result
lsl_add r5, r0, r2, 2
lw r7, r5, 0
;add
add r7, r7, r3
sw r5, 0, r7
