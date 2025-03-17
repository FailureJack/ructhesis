;Result[k]+=SubLUT[Vector[j]&0xF][MatRow[k]]
;Result:r0, k:r2, SubLUT[Vector[j]&0xF]:r4, MatRow:r6

;MatRow
lbui r1, r6, r2
;SubLUT
lwi r3, r4, r1, 2
;add
fmla r0, r2, 2, r3

