;Result[IndexRow[l]]+=product
;Result:r0, IndexRow:r2, l:r4, product: r6

;IndexRow
lsl_add r1, r2, r4, 1
lhu r1, r1, 0

;Result
lsl_add r3, r0, r1, 2
lw r5, r3, 0

;add
add r5, r5, r6
sw r3, 0, r5



