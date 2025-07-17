#!/bin/bash
# Quick launch script for the 2D Racing Game

echo "🎮 2D Racing Game - Quick Launch"
echo "================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
echo "🔧 Setting up environment..."
source .venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# Check if track images exist
if [ ! -f "track1_visual.png" ] || [ ! -f "track1_mask.png" ]; then
    echo "🛣️  Creating sample track images..."
    python create_track.py
fi

# Check if car sprites exist
if [ ! -f "car_sports.png" ] || [ ! -f "car_truck.png" ]; then
    echo "🚗 Creating car sprites..."
    python create_sprites.py
fi

# Launch the game
echo "🚀 Starting the racing game..."
echo ""
echo "Controls:"
echo "  Player 1: WASD"
echo "  Player 2: Arrow Keys"
echo "  U/J: Adjust Player 1 turn speed"
echo "  I/K: Adjust Player 1 acceleration"
echo ""
python main.py
