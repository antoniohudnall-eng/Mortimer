#!/usr/bin/env python3
"""
GPIO Control Skill - General Purpose Input/Output Interface

Controls digital and analog pins for:
- Sensors (temperature, pressure, proximity)
- LEDs (status indicators, expression)
- Switches (emergency stop, mode selection)
- Communication (SPI, I2C, UART)

Integrates with BHSI (Body Hardware System Interface) to allow
agents to control low-level hardware alongside actuators.

Different from BCSA V4:
- BCSA V4 = High-torque actuators (joints, motors)
- GPIO = Low-level digital/analog control (sensors, indicators)

Both are part of complete body hardware interface.
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class GPIOMode(Enum):
    INPUT = "input"
    OUTPUT = "output"
    PWM = "pwm"
    ANALOG = "analog"


@dataclass
class GPIOPin:
    """Represents a single GPIO pin."""
    pin_number: int
    mode: GPIOMode
    value: float = 0.0  # 0.0 or 1.0 for digital, 0-255 for PWM, 0-1023 for analog
    label: str = ""      # Human-readable label
    
    # Limits
    min_value: float = 0.0
    max_value: float = 1.0
    
    # Metadata
    description: str = ""
    last_update: float = field(default_factory=time.time)


class GPIOController:
    """
    GPIO Controller for AOS-H1 robot.
    
    Manages digital/analog pins for sensors and indicators.
    Separate from BCSA V4 actuators (which handle motors/joints).
    
    Pin Map (AOS-H1):
    ==========
    Digital Pins (0-15):
      0-3:   Status LEDs (head, torso, left arm, right arm)
      4-7:   Emergency stop switches (distributed)
      8-11:  Mode selectors (4-position switch)
      12-15: Reserved
    
    PWM Pins (16-23):
      16-17: Eye brightness control (left, right)
      18-19: Expression LEDs (brow left, brow right)
      20-23: Reserved for servos
    
    Analog Input (24-31):
      24:    Temperature sensor (core)
      25:    Temperature sensor (right arm)
      26:    Temperature sensor (left arm)
      27:    Pressure sensor (right hand)
      28:    Pressure sensor (left hand)
      29:    Proximity sensor (head)
      30-31: Reserved
    
    I2C/SPI:
      Bus 0: IMU (inertial measurement unit)
      Bus 1: External sensors
    """
    
    def __init__(self):
        self.pins: Dict[int, GPIOPin] = {}
        self._init_default_pins()
        
        # Connection state
        self.connected = False
        self.last_update = time.time()
        
        # Statistics
        self.reads = 0
        self.writes = 0
    
    def _init_default_pins(self):
        """Initialize default GPIO pin configuration."""
        
        # Digital outputs - Status LEDs
        for i, label in enumerate(['head_status', 'torso_status', 'left_arm_status', 'right_arm_status']):
            self.pins[i] = GPIOPin(
                pin_number=i,
                mode=GPIOMode.OUTPUT,
                label=label,
                description=f"Status LED on {label.replace('_status', '')}"
            )
        
        # Digital inputs - Emergency stops
        for i, label in enumerate(['emergency_stop_head', 'emergency_stop_torso', 
                                   'emergency_stop_right', 'emergency_stop_left'], start=4):
            self.pins[i] = GPIOPin(
                pin_number=i,
                mode=GPIOMode.INPUT,
                label=label,
                description="Emergency stop switch"
            )
        
        # PWM outputs - Expression/eyes
        for i, label in enumerate(['eye_left', 'eye_right', 'brow_left', 'brow_right'], start=16):
            self.pins[i] = GPIOPin(
                pin_number=i,
                mode=GPIOMode.PWM,
                max_value=255.0,
                label=label,
                description=f"{label.replace('_', ' ').title()} brightness control"
            )
        
        # Analog inputs - Sensors
        sensor_pins = [
            (24, 'temperature_core', 'Core body temperature'),
            (25, 'temperature_right_arm', 'Right arm temperature'),
            (26, 'temperature_left_arm', 'Left arm temperature'),
            (27, 'pressure_right_hand', 'Right hand pressure sensor'),
            (28, 'pressure_left_hand', 'Left hand pressure sensor'),
            (29, 'proximity_head', 'Head proximity sensor'),
        ]
        
        for pin_num, label, desc in sensor_pins:
            self.pins[pin_num] = GPIOPin(
                pin_number=pin_num,
                mode=GPIOMode.ANALOG,
                max_value=1023.0,
                label=label,
                description=desc
            )
    
    def set_pin_mode(self, pin_number: int, mode: GPIOMode) -> bool:
        """Set pin mode (input/output/PWM/analog)."""
        if pin_number not in self.pins:
            return False
        
        self.pins[pin_number].mode = mode
        return True
    
    def digital_write(self, pin_number: int, value: bool) -> bool:
        """
        Write digital value to pin.
        
        Args:
            pin_number: GPIO pin number
            value: True (HIGH) or False (LOW)
        
        Returns:
            True if successful
        """
        if pin_number not in self.pins:
            return False
        
        pin = self.pins[pin_number]
        if pin.mode not in [GPIOMode.OUTPUT, GPIOMode.PWM]:
            return False
        
        pin.value = 1.0 if value else 0.0
        pin.last_update = time.time()
        self.writes += 1
        
        return True
    
    def digital_read(self, pin_number: int) -> Optional[bool]:
        """
        Read digital value from pin.
        
        Args:
            pin_number: GPIO pin number
        
        Returns:
            True (HIGH), False (LOW), or None if error
        """
        if pin_number not in self.pins:
            return None
        
        pin = self.pins[pin_number]
        if pin.mode not in [GPIOMode.INPUT, GPIOMode.ANALOG]:
            return None
        
        # Simulate reading
        if pin.mode == GPIOMode.ANALOG:
            # Convert analog to digital (threshold at 50%)
            return pin.value > (pin.max_value / 2)
        
        self.reads += 1
        return pin.value > 0.5
    
    def analog_write(self, pin_number: int, value: float) -> bool:
        """
        Write analog/PWM value to pin.
        
        Args:
            pin_number: GPIO pin number
            value: 0.0 to max_value (typically 0-255 for PWM)
        
        Returns:
            True if successful
        """
        if pin_number not in self.pins:
            return False
        
        pin = self.pins[pin_number]
        if pin.mode not in [GPIOMode.PWM, GPIOMode.ANALOG]:
            return False
        
        # Clamp to limits
        pin.value = max(pin.min_value, min(pin.max_value, value))
        pin.last_update = time.time()
        self.writes += 1
        
        return True
    
    def analog_read(self, pin_number: int) -> Optional[float]:
        """
        Read analog value from pin.
        
        Args:
            pin_number: GPIO pin number
        
        Returns:
            Analog value (0-max_value) or None if error
        """
        if pin_number not in self.pins:
            return None
        
        pin = self.pins[pin_number]
        if pin.mode != GPIOMode.ANALOG:
            return None
        
        # Simulate reading with some noise
        import random
        noise = random.uniform(-5, 5)
        value = pin.value + noise
        value = max(pin.min_value, min(pin.max_value, value))
        
        self.reads += 1
        return value
    
    def set_expression(self, expression: str, intensity: float = 1.0) -> bool:
        """
        Set facial expression using PWM LEDs.
        
        Args:
            expression: 'neutral', 'happy', 'sad', 'surprised', 'alert'
            intensity: 0.0 to 1.0 brightness
        
        Returns:
            True if successful
        """
        brightness = intensity * 255
        
        expressions = {
            'neutral': {'eye_left': brightness, 'eye_right': brightness, 
                       'brow_left': 0, 'brow_right': 0},
            'happy': {'eye_left': brightness, 'eye_right': brightness,
                     'brow_left': 0, 'brow_right': 0},  # Relaxed brows
            'sad': {'eye_left': brightness * 0.5, 'eye_right': brightness * 0.5,
                   'brow_left': brightness * 0.3, 'brow_right': brightness * 0.3},  # Furrowed
            'surprised': {'eye_left': brightness, 'eye_right': brightness,
                        'brow_left': brightness, 'brow_right': brightness},  # Raised
            'alert': {'eye_left': brightness, 'eye_right': brightness,
                     'brow_left': brightness * 0.5, 'brow_right': brightness * 0.5},
        }
        
        if expression not in expressions:
            return False
        
        # Find PWM pins by label
        label_to_pin = {pin.label: pin.pin_number for pin in self.pins.values()}
        
        for label, value in expressions[expression].items():
            if label in label_to_pin:
                self.analog_write(label_to_pin[label], value)
        
        return True
    
    def read_temperature(self, location: str = 'core') -> Optional[float]:
        """
        Read temperature from sensor.
        
        Args:
            location: 'core', 'right_arm', 'left_arm'
        
        Returns:
            Temperature in Celsius or None if error
        """
        label_map = {
            'core': 'temperature_core',
            'right_arm': 'temperature_right_arm',
            'left_arm': 'temperature_left_arm'
        }
        
        if location not in label_map:
            return None
        
        label = label_map[location]
        pin_num = None
        for num, pin in self.pins.items():
            if pin.label == label:
                pin_num = num
                break
        
        if pin_num is None:
            return None
        
        # Read analog value and convert to temperature
        raw = self.analog_read(pin_num)
        if raw is None:
            return None
        
        # Simplified conversion: 0-1023 maps to 0-100°C
        temp = (raw / 1023.0) * 100.0
        return temp
    
    def check_emergency_stops(self) -> Dict[str, bool]:
        """
        Check all emergency stop switches.
        
        Returns:
            Dict of switch labels and states (True = pressed/stop)
        """
        stops = {}
        for pin in self.pins.values():
            if 'emergency_stop' in pin.label:
                value = self.digital_read(pin.pin_number)
                stops[pin.label] = value if value is not None else False
        
        return stops
    
    def get_pin_map(self) -> Dict:
        """Get complete pin map."""
        return {
            'digital_outputs': [p.pin_number for p in self.pins.values() if p.mode == GPIOMode.OUTPUT],
            'digital_inputs': [p.pin_number for p in self.pins.values() if p.mode == GPIOMode.INPUT],
            'pwm_outputs': [p.pin_number for p in self.pins.values() if p.mode == GPIOMode.PWM],
            'analog_inputs': [p.pin_number for p in self.pins.values() if p.mode == GPIOMode.ANALOG],
            'pins': {num: {
                'label': pin.label,
                'mode': pin.mode.value,
                'value': pin.value,
                'description': pin.description
            } for num, pin in self.pins.items()}
        }
    
    def get_stats(self) -> Dict:
        """Get controller statistics."""
        return {
            'total_pins': len(self.pins),
            'digital_outputs': len([p for p in self.pins.values() if p.mode == GPIOMode.OUTPUT]),
            'digital_inputs': len([p for p in self.pins.values() if p.mode == GPIOMode.INPUT]),
            'pwm_outputs': len([p for p in self.pins.values() if p.mode == GPIOMode.PWM]),
            'analog_inputs': len([p for p in self.pins.values() if p.mode == GPIOMode.ANALOG]),
            'reads': self.reads,
            'writes': self.writes
        }


# Skill handler
def gpio_handler(input_data: Dict) -> Dict:
    """
    GPIO skill handler.
    
    Input:
        action: 'write' | 'read' | 'set_expression' | 'read_temp' | 'check_stops' | 'map' | 'stats'
        pin: pin number (for write/read)
        value: value to write
        expression: expression name (for set_expression)
        location: temperature location (for read_temp)
    
    Output:
        success: bool
        value: read value (for read actions)
        stats: controller stats (for stats action)
    """
    if not hasattr(gpio_handler, '_gpio'):
        gpio_handler._gpio = GPIOController()
    
    gpio = gpio_handler._gpio
    action = input_data.get('action', 'stats')
    
    if action == 'write':
        pin = input_data.get('pin')
        value = input_data.get('value')
        mode = input_data.get('mode', 'digital')
        
        if mode == 'digital':
            success = gpio.digital_write(pin, bool(value))
        else:  # analog/PWM
            success = gpio.analog_write(pin, float(value))
        
        return {'success': success, 'pin': pin, 'value': value}
    
    elif action == 'read':
        pin = input_data.get('pin')
        mode = input_data.get('mode', 'digital')
        
        if mode == 'digital':
            value = gpio.digital_read(pin)
        else:
            value = gpio.analog_read(pin)
        
        return {'success': value is not None, 'pin': pin, 'value': value}
    
    elif action == 'set_expression':
        expression = input_data.get('expression', 'neutral')
        intensity = input_data.get('intensity', 1.0)
        success = gpio.set_expression(expression, intensity)
        return {'success': success, 'expression': expression, 'intensity': intensity}
    
    elif action == 'read_temp':
        location = input_data.get('location', 'core')
        temp = gpio.read_temperature(location)
        return {'success': temp is not None, 'location': location, 'temperature': temp}
    
    elif action == 'check_stops':
        stops = gpio.check_emergency_stops()
        return {'success': True, 'emergency_stops': stops, 'any_pressed': any(stops.values())}
    
    elif action == 'map':
        return {'success': True, 'pin_map': gpio.get_pin_map()}
    
    else:  # stats
        return {'success': True, 'stats': gpio.get_stats()}


if __name__ == '__main__':
    print("🔌 GPIO Control for AOS-H1")
    print("=" * 60)
    
    gpio = GPIOController()
    
    # Show pin map
    print("\n[1] GPIO Pin Map:")
    stats = gpio.get_stats()
    print(f"   Digital Outputs: {stats['digital_outputs']}")
    print(f"   Digital Inputs:  {stats['digital_inputs']}")
    print(f"   PWM Outputs:     {stats['pwm_outputs']}")
    print(f"   Analog Inputs:   {stats['analog_inputs']}")
    
    # Set expression
    print("\n[2] Setting Expression:")
    gpio.set_expression('happy', intensity=0.8)
    print("   Expression: happy @ 80% brightness")
    
    # Read temperature
    print("\n[3] Reading Temperature Sensors:")
    for location in ['core', 'right_arm', 'left_arm']:
        temp = gpio.read_temperature(location)
        print(f"   {location}: {temp:.1f}°C")
    
    # Check emergency stops
    print("\n[4] Emergency Stop Status:")
    stops = gpio.check_emergency_stops()
    for label, pressed in stops.items():
        status = "🔴 PRESSED" if pressed else "✅ CLEAR"
        print(f"   {label}: {status}")
    
    print("\n✅ GPIO Controller ready for integration!")
