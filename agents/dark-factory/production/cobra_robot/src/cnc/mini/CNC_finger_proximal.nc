; COBRA Finger Segment - proximal
; Length: 8.25mm, Width: 12mm

G21
G90
G17

G0 Z50
M3 S20000

; Cut profile
G0 X-6.000 Y0
G1 Z-8 F500
G1 X6.000 F1500
G1 Y8.250
G1 X-6.000
G1 Y0

; Tendon channel
G0 X0 Y4.125
G1 Z-8 F500
G0 Z50

; Pivot holes
G81 X0 Y0 Z-8 R2 F500
G81 X0 Y8.250 Z-8 R2 F500

M5
G0 X0 Y0
M30