;temp+=∗(Offset[l] +SubMat[l][k]*ele_width)
;temp:r0, Offset:r2, l:r4, SubMat:r6, k:r8, ele_width:4

;Offset
ldi r1, r2, r4, 3
;SubMat
lsl_add r3, r8, r4, 7
lwi r5, r6, r3, 0
;add
fmla r0, r1, r5, 2

