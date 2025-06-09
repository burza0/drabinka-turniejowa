"""
SECTRO Live Timing - Frame Parser
Based on official SECTRO documentation and C++ reference code

Supported frame formats:
- CZLxtimestamp - Line crossing, input x
- CHLxtimestamp - Line release, input x  
- VCCxxtimestamp - Voltage measurement
"""

import re
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SectroFrame:
    """Parsed SECTRO frame data"""
    frame_type: str         # 'CZL', 'CHL', 'VCC'
    input_number: int       # 1-8 for timing, 0 for sync
    timestamp: float        # Seconds since midnight
    raw_frame: str          # Original frame string
    is_sync: bool          # True if sync frame (input 0)
    is_valid: bool         # True if frame parsed successfully
    measurement_type: str   # 'START', 'FINISH', 'SPLIT', 'SYNC', 'VOLTAGE'


class SectroParser:
    """
    Parser for SECTRO timing device frames
    
    Usage:
        parser = SectroParser(start_input=1, finish_input=4)
        frame = parser.parse_frame("CZL1123456789")
        if frame.is_valid:
            print(f"START detected at {frame.timestamp}s")
    """
    
    def __init__(self, start_input: int = 1, finish_input: int = 4):
        """
        Initialize parser with input configuration
        
        Args:
            start_input: Input number for START line (default: 1)
            finish_input: Input number for FINISH line (default: 4)
        """
        self.start_input = start_input
        self.finish_input = finish_input
        
        # Frame validation regex patterns
        self.timing_pattern = re.compile(r'^(CZL|CHL)(\d)(\d{9})$')
        self.voltage_pattern = re.compile(r'^VCC(\d{2})(\d{9})$')
        
    def parse_frame(self, raw_frame: str) -> SectroFrame:
        """
        Parse single SECTRO frame
        
        Args:
            raw_frame: Raw frame string from serial port
            
        Returns:
            SectroFrame object with parsed data
        """
        raw_frame = raw_frame.strip()
        
        # Try parsing timing frame (CZL/CHL)
        timing_match = self.timing_pattern.match(raw_frame)
        if timing_match:
            return self._parse_timing_frame(timing_match, raw_frame)
            
        # Try parsing voltage frame (VCC)
        voltage_match = self.voltage_pattern.match(raw_frame)
        if voltage_match:
            return self._parse_voltage_frame(voltage_match, raw_frame)
            
        # Invalid frame
        return SectroFrame(
            frame_type='UNKNOWN',
            input_number=0,
            timestamp=0.0,
            raw_frame=raw_frame,
            is_sync=False,
            is_valid=False,
            measurement_type='INVALID'
        )
    
    def _parse_timing_frame(self, match: re.Match, raw_frame: str) -> SectroFrame:
        """Parse timing frame (CZL/CHL format)"""
        frame_type = match.group(1)  # 'CZL' or 'CHL'
        input_str = match.group(2)   # Input number as string
        timestamp_str = match.group(3)  # 9-digit timestamp
        
        try:
            input_number = int(input_str)
            timestamp = self._decode_timestamp(timestamp_str)
            
            # Determine measurement type
            measurement_type = self._get_measurement_type(frame_type, input_number)
            is_sync = (input_number == 0)
            
            return SectroFrame(
                frame_type=frame_type,
                input_number=input_number,
                timestamp=timestamp,
                raw_frame=raw_frame,
                is_sync=is_sync,
                is_valid=True,
                measurement_type=measurement_type
            )
            
        except ValueError as e:
            return self._create_error_frame(raw_frame, f"Parsing error: {e}")
    
    def _parse_voltage_frame(self, match: re.Match, raw_frame: str) -> SectroFrame:
        """Parse voltage measurement frame (VCC format)"""
        input_str = match.group(1)   # Input number (2 digits)
        voltage_str = match.group(2)  # Voltage value
        
        try:
            input_number = int(input_str)
            voltage_value = float(voltage_str)
            
            return SectroFrame(
                frame_type='VCC',
                input_number=input_number,
                timestamp=voltage_value,  # Store voltage in timestamp field
                raw_frame=raw_frame,
                is_sync=False,
                is_valid=True,
                measurement_type='VOLTAGE'
            )
            
        except ValueError as e:
            return self._create_error_frame(raw_frame, f"Voltage parsing error: {e}")
    
    def _decode_timestamp(self, timestamp_str: str) -> float:
        """
        Decode SECTRO timestamp format: HHMMSSMMM
        
        Args:
            timestamp_str: 9-character timestamp string
            
        Returns:
            Seconds since midnight as float
        """
        if len(timestamp_str) != 9:
            raise ValueError(f"Invalid timestamp length: {len(timestamp_str)}")
        
        try:
            hours = int(timestamp_str[0:2])
            minutes = int(timestamp_str[2:4])
            seconds = int(timestamp_str[4:6])
            milliseconds = int(timestamp_str[6:9])
            
            # Validate ranges
            if not (0 <= hours <= 23):
                raise ValueError(f"Invalid hours: {hours}")
            if not (0 <= minutes <= 59):
                raise ValueError(f"Invalid minutes: {minutes}")
            if not (0 <= seconds <= 59):
                raise ValueError(f"Invalid seconds: {seconds}")
            if not (0 <= milliseconds <= 999):
                raise ValueError(f"Invalid milliseconds: {milliseconds}")
            
            # Convert to total seconds since midnight
            total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
            return total_seconds
            
        except ValueError as e:
            raise ValueError(f"Timestamp decode error: {e}")
    
    def _get_measurement_type(self, frame_type: str, input_number: int) -> str:
        """Determine measurement type based on frame type and input"""
        if input_number == 0:
            return 'SYNC'
        elif frame_type == 'CHL':
            return 'RELEASE'  # Line release (not used for timing)
        elif input_number == self.start_input:
            return 'START'
        elif input_number == self.finish_input:
            return 'FINISH'
        else:
            return 'SPLIT'  # Other inputs are split times
    
    def _create_error_frame(self, raw_frame: str, error_msg: str) -> SectroFrame:
        """Create error frame for debugging"""
        return SectroFrame(
            frame_type='ERROR',
            input_number=0,
            timestamp=0.0,
            raw_frame=raw_frame,
            is_sync=False,
            is_valid=False,
            measurement_type='ERROR'
        )
    
    def is_start_frame(self, frame: SectroFrame) -> bool:
        """Check if frame represents a START measurement"""
        return frame.is_valid and frame.measurement_type == 'START'
    
    def is_finish_frame(self, frame: SectroFrame) -> bool:
        """Check if frame represents a FINISH measurement"""
        return frame.is_valid and frame.measurement_type == 'FINISH'
    
    def is_timing_frame(self, frame: SectroFrame) -> bool:
        """Check if frame is a valid timing measurement (START/FINISH/SPLIT)"""
        return frame.is_valid and frame.measurement_type in ['START', 'FINISH', 'SPLIT']
    
    def calculate_race_time(self, start_frame: SectroFrame, finish_frame: SectroFrame) -> Optional[float]:
        """
        Calculate race time from start and finish frames
        
        Args:
            start_frame: START measurement frame
            finish_frame: FINISH measurement frame
            
        Returns:
            Race time in seconds, or None if invalid
        """
        if not (self.is_start_frame(start_frame) and self.is_finish_frame(finish_frame)):
            return None
        
        race_time = finish_frame.timestamp - start_frame.timestamp
        
        # Handle day rollover (race crossing midnight)
        if race_time < 0:
            race_time += 24 * 3600  # Add 24 hours
        
        return race_time
    
    def format_time(self, seconds: float) -> str:
        """Format seconds to MM:SS.mmm format"""
        if seconds < 0:
            return "INVALID"
        
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        
        return f"{minutes:02d}:{remaining_seconds:06.3f}"


# Example usage and testing
if __name__ == "__main__":
    # Test the parser
    parser = SectroParser(start_input=1, finish_input=4)
    
    test_frames = [
        "CZL1123456789",  # START at 12:34:56.789
        "CZL4123459123",  # FINISH at 12:34:59.123  
        "CZL0000000000",  # SYNC frame
        "VCC1500000000",  # Voltage measurement
        "INVALID_FRAME",  # Invalid frame
    ]
    
    for frame_str in test_frames:
        frame = parser.parse_frame(frame_str)
        print(f"Frame: {frame_str}")
        print(f"  Type: {frame.measurement_type}")
        print(f"  Valid: {frame.is_valid}")
        print(f"  Timestamp: {frame.timestamp}")
        print(f"  Formatted: {parser.format_time(frame.timestamp)}")
        print()
    
    # Test race time calculation
    start = parser.parse_frame("CZL1123456000")  # 12:34:56.000
    finish = parser.parse_frame("CZL4123459500")  # 12:34:59.500
    
    race_time = parser.calculate_race_time(start, finish)
    if race_time:
        print(f"Race time: {parser.format_time(race_time)}") 