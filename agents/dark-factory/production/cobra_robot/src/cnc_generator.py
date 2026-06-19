#!/usr/bin/env python3
"""
COBRA-SKELETON CNC Generator
Generates G-code toolpaths for foam core machining
"""

import os
import math


class CNCToolpathGenerator:
    """Generate G-code for Rohacell foam cutting"""
    
    def __init__(self, output_dir="cnc"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Tool parameters
        self.tool_dia = 2.0  # mm
        self.tool_radius = self.tool_dia / 2
        self.spindle_speed = 20000  # RPM
        self.feed_rate = 1500  # mm/min
        self.plunge_rate = 500  # mm/min
        self.stepdown = 5.0  # mm per pass
        
    def generate_vertebra_cnc(self, vid, region, height, od, has_battery, has_solar):
        """Generate G-code for a single vertebra"""
        
        gcode = []
        gcode.append(f"; COBRA Vertebra - {region} V{vid}")
        gcode.append(f"; Material: Rohacell IG-51 {height}mm")
        gcode.append(f"; Tool: {self.tool_dia}mm carbide end mill")
        gcode.append("")
        
        # Header
        gcode.extend([
            "G21",  # Metric
            "G90",  # Absolute positioning
            "G17",  # XY plane
            "G54",  # Work coordinate system
            "",
            "; Safe start",
            "G0 Z50",
            "G0 X0 Y0",
            "M3 S20000",  # Spindle on
            "G4 P2000",   # Dwell 2s
            "",
        ])
        
        # Calculate passes
        num_passes = int(math.ceil(height / self.stepdown))
        
        # Outer profile
        gcode.append("; Cut outer profile")
        radius = od / 2 - self.tool_radius
        
        for pass_num in range(1, num_passes + 1):
            z_depth = -min(pass_num * self.stepdown, height)
            gcode.append(f"")
            gcode.append(f"; Pass {pass_num}/{num_passes}, Z={z_depth}")
            
            # Helical entry
            gcode.append(f"G0 X{radius:.3f} Y0")
            gcode.append(f"G1 Z{z_depth:.3f} F{self.plunge_rate}")
            
            # Circle
            gcode.append(f"G2 I-{radius:.3f} J0 F{self.feed_rate}")
        
        # Battery cavities (if applicable)
        if has_battery:
            gcode.append("")
            gcode.append("; Battery cavities")
            
            cavity_width = 20.0
            cavity_depth = 65.0
            offset = (od - cavity_width) / 4
            
            for cavity_num in range(2):
                angle = cavity_num * 180
                rad = math.radians(angle)
                cx = offset * math.cos(rad)
                cy = offset * math.sin(rad)
                
                gcode.append(f"")
                gcode.append(f"; Cavity {cavity_num + 1}")
                
                # Slot for battery
                for pass_num in range(1, num_passes + 1):
                    z_depth = -min(pass_num * self.stepdown, height)
                    
                    gcode.append(f"G0 X{cx + cavity_depth/2:.3f} Y{cy:.3f}")
                    gcode.append(f"G1 Z{z_depth:.3f} F{self.plunge_rate}")
                    gcode.append(f"G1 X{cx - cavity_depth/2:.3f} F{self.feed_rate}")
        
        # Solar panel cavity (if applicable)
        if has_solar:
            gcode.append("")
            gcode.append("; Solar panel cavity")
            
            panel_width = 50.0
            panel_height = 30.0
            
            gcode.append(f"G0 X{-panel_width/2:.3f} Y{od/2 - 5:.3f}")
            
            for pass_num in range(1, 3):  # Shallow cavity
                z_depth = -3 * pass_num
                gcode.append(f"G1 Z{z_depth:.3f} F{self.plunge_rate}")
                gcode.append(f"G1 X{panel_width/2:.3f} F{self.feed_rate}")
                gcode.append(f"G1 Y{od/2 - 5 + panel_height:.3f}")
                gcode.append(f"G1 X{-panel_width/2:.3f}")
                gcode.append(f"G1 Y{od/2 - 5:.3f}")
        
        # Mounting holes
        gcode.append("")
        gcode.append("; Mounting holes")
        
        hole_positions = [
            (od/2 - 5, 0),
            (-(od/2 - 5), 0),
            (0, od/2 - 5),
            (0, -(od/2 - 5)),
        ]
        
        for i, (hx, hy) in enumerate(hole_positions):
            gcode.append(f"G81 X{hx:.3f} Y{hy:.3f} Z-{height:.3f} R2 F{self.plunge_rate}")
        
        # Footer
        gcode.extend([
            "",
            "; End of program",
            "G0 Z50",
            "M5",  # Spindle off
            "G0 X0 Y0",
            "M30",  # Program end
        ])
        
        return "\n".join(gcode)
    
    def generate_finger_cnc(self, seg_type, length):
        """Generate G-code for finger segment"""
        
        width = {"proximal": 12, "middle": 10, "distal": 8}.get(seg_type, 10)
        
        gcode = [
            f"; COBRA Finger Segment - {seg_type}",
            f"; Length: {length}mm, Width: {width}mm",
            "",
            "G21",
            "G90",
            "G17",
            "",
            "G0 Z50",
            "M3 S20000",
            "",
            "; Cut profile",
            f"G0 X{-width/2:.3f} Y0",
            "G1 Z-8 F500",
            f"G1 X{width/2:.3f} F1500",
            f"G1 Y{length:.3f}",
            f"G1 X{-width/2:.3f}",
            "G1 Y0",
            "",
            "; Tendon channel",
            f"G0 X0 Y{length/2:.3f}",
            "G1 Z-8 F500",
            "G0 Z50",
            "",
            "; Pivot holes",
            "G81 X0 Y0 Z-8 R2 F500",
            f"G81 X0 Y{length:.3f} Z-8 R2 F500",
            "",
            "M5",
            "G0 X0 Y0",
            "M30",
        ]
        
        return "\n".join(gcode)
    
    def generate_sheet_layout(self, model_size="midi"):
        """Generate DXF-style cutting layout for carbon fiber sheets"""
        
        scale = {"mini": 0.33, "midi": 1.0, "max": 2.0}.get(model_size, 1.0)
        
        layout = []
        layout.append("; Carbon Fiber Cutting Layout")
        layout.append(f"; Model: {model_size.upper()}")
        layout.append("; Material: CF 200g/m2 Twill")
        layout.append("")
        
        # Vertebra skins
        for i in range(25):
            od = (30 + i * 0.8) * scale  # Graduated sizing
            layout.append(f"CIRCLE {i*60 + 30} 30 {od/2}  ; V{i:02d}")
        
        # Finger wraps
        layout.append("")
        layout.append("; Finger segments (rectangular strips)")
        for i in range(15):
            layout.append(f"RECT {i*15} 100 12 25  ; Finger {i+1}")
        
        return "\n".join(layout)
    
    def generate_all_files(self, model_size="midi"):
        """Generate all CNC files"""
        
        files_created = []
        
        scale = {"mini": 0.33, "midi": 1.0, "max": 2.0}.get(model_size, 1.0)
        
        # Vertebrae G-code
        # C1-C7
        for i in range(7):
            filename = f"CNC_V{i:02d}_C{i+1}.nc"
            filepath = os.path.join(self.output_dir, model_size, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                f.write(self.generate_vertebra_cnc(
                    i, f"C{i+1}", 15*scale, 30*scale, False, False
                ))
            files_created.append(filename)
        
        # T1-T12
        for i in range(7, 19):
            filename = f"CNC_V{i:02d}_T{i-6}.nc"
            filepath = os.path.join(self.output_dir, model_size, filename)
            
            has_bat = model_size != "mini"
            with open(filepath, 'w') as f:
                f.write(self.generate_vertebra_cnc(
                    i, f"T{i-6}", 20*scale, 40*scale, has_bat, True
                ))
            files_created.append(filename)
        
        # L1-L5
        for i in range(19, 24):
            filename = f"CNC_V{i:02d}_L{i-18}.nc"
            filepath = os.path.join(self.output_dir, model_size, filename)
            
            has_bat = model_size != "mini"
            with open(filepath, 'w') as f:
                f.write(self.generate_vertebra_cnc(
                    i, f"L{i-18}", 25*scale, 45*scale, has_bat, False
                ))
            files_created.append(filename)
        
        # S1
        filename = "CNC_V24_S1.nc"
        filepath = os.path.join(self.output_dir, model_size, filename)
        has_bat = model_size != "mini"
        with open(filepath, 'w') as f:
            f.write(self.generate_vertebra_cnc(
                24, "S1", 30*scale, 50*scale, has_bat, False
            ))
        files_created.append(filename)
        
        # Fingers
        for seg_type in ["proximal", "middle", "distal"]:
            length = {"proximal": 25, "middle": 20, "distal": 15}.get(seg_type, 20)
            filename = f"CNC_finger_{seg_type}.nc"
            filepath = os.path.join(self.output_dir, model_size, filename)
            
            with open(filepath, 'w') as f:
                f.write(self.generate_finger_cnc(seg_type, length * scale))
            files_created.append(filename)
        
        # CF cutting layout
        filename = f"CF_layout_{model_size}.dxf"
        filepath = os.path.join(self.output_dir, model_size, filename)
        
        with open(filepath, 'w') as f:
            f.write(self.generate_sheet_layout(model_size))
        files_created.append(filename)
        
        return files_created


def main():
    print("=" * 70)
    print("🐍 COBRA-SKELETON CNC Generator")
    print("=" * 70)
    
    generator = CNCToolpathGenerator("cnc")
    
    for model_size in ["mini", "midi", "max"]:
        print("\n📐 Generating " + model_size.upper() + " CNC files...")
        
        files = generator.generate_all_files(model_size)
        
        print("   Created " + str(len(files)) + " G-code files")
        print("   Location: cnc/" + model_size + "/")
        
        # Group by type
        vertebrae = [f for f in files if f.startswith("CNC_V")]
        fingers = [f for f in files if "finger" in f]
        
        print("      Vertebrae: " + str(len(vertebrae)) + " files")
        print("      Fingers: " + str(len(fingers)) + " files")
        print("      CF layout: 1 file")
    
    print("\n" + "=" * 70)
    print("✅ CNC Generation Complete")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Load G-code into CNC controller")
    print("2. Secure Rohacell sheet with vacuum table")
    print("3. Run first toolpath (air cut test)")
    print("4. Cut all vertebrae cores")
    print("5. Apply CF skins using vacuum infusion")


if __name__ == "__main__":
    main()
