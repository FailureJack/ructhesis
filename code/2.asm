;temp+=∗(Offset[l] +SubMat[l][k]*ele_width)
;temp:r0, Offset:r2, l:r4, SubMat:r6, k:r8, ele_width:4

;Offset
lsl_add r1, r2, r4, 3
ld r1, r1, 0
;SubMat
lsl_add r3, r8, r4, 7
add r5, r6, r3
lbu r5, r5, 0
;addr
lsl_add r7, r1, r5, 2
lw r7, r7, 0
;add
add r0, r0, r7

