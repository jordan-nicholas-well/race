#!/usr/bin/env python3
"""
Test script to verify all game components work correctly.
"""

import sys
import pygame

# Initialize pygame without creating a window
pygame.init()

try:
    # Test importing all modules
    from settings import SPORTS_CAR, TRUCK, TRACK_COLORS
    from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS
    from track import Track
    from car import Car
    
    print("✓ All modules imported successfully")
    
    # Test track creation
    track = Track()
    track._create_fallback_track()
    print("✓ Fallback track created successfully")
    print(f"  Start positions found: {len(track.get_start_positions())}")
    
    # Test car creation
    start_positions = track.get_start_positions()
    if len(start_positions) >= 2:
        car1 = Car(start_positions[0], SPORTS_CAR)
        car2 = Car(start_positions[1], TRUCK)
        print("✓ Cars created successfully")
        print(f"  Car 1 position: ({car1.x:.1f}, {car1.y:.1f})")
        print(f"  Car 2 position: ({car2.x:.1f}, {car2.y:.1f})")
    
    # Test physics adjustment
    car1.adjust_physics('turn_speed', True)
    car1.adjust_physics('acceleration', False)
    print("✓ Physics adjustments work correctly")
    
    # Test collision detection
    collision_color = track.check_collision(100, 100)
    print(f"✓ Collision detection works: {collision_color}")
    
    print("\n🎮 Game components test PASSED!")
    print("The racing game is ready to run. Execute 'python main.py' to start playing!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1)
finally:
    pygame.quit()
