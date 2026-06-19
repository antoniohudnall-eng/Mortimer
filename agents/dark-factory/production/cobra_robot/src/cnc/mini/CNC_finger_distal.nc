; COBRA Finger Segment - distal
; Length: 4.95mm, Width: 8mm

G21
G90
G17

G0 Z50
M3 S20000

; Cut profile
G0 X-4.000 Y0
G1 Z-8 F500
G1 X4.000 F1500
G1 Y4.950
G1 X-4.000
G1 Y0

; Tendon channel
G0 X0 Y2.475
G1 Z-8 F500
G0 Z50

; Pivot holes
G81 X0 Y0 Z-8 R2 F500
G81 X0 Y4.950 Z-8 R2 F500

M5
G0 X0 Y0
M30