; COBRA Vertebra - C4 V3
; Material: Rohacell IG-51 4.95mm
; Tool: 2.0mm carbide end mill

G21
G90
G17
G54

; Safe start
G0 Z50
G0 X0 Y0
M3 S20000
G4 P2000

; Cut outer profile

; Pass 1/1, Z=-4.95
G0 X3.950 Y0
G1 Z-4.950 F500
G2 I-3.950 J0 F1500

; Mounting holes
G81 X-0.050 Y0.000 Z-4.950 R2 F500
G81 X0.050 Y0.000 Z-4.950 R2 F500
G81 X0.000 Y-0.050 Z-4.950 R2 F500
G81 X0.000 Y0.050 Z-4.950 R2 F500

; End of program
G0 Z50
M5
G0 X0 Y0
M30