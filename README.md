# Rock, Paper, Scissors - AI Detection

This project uses YOLO to detect and determine the winner in a real-time 'Rock, Paper, Scissors' game using a webcam.

## Features

- Real-time detection using YOLO
- Automatic winner determination
- Countdown before result calculation
- Score tracking for two players

## Installation

1. Clone the repository:
    
    ```sh
    gh repo clone AmirSalajegheh/Rock-Paper-Scissor-yolov11
    ```
    
2. Navigate to the project directory:
    
    ```sh
    cd Rock-Paper-Scissor-yolov11
    ```
    
3. Install dependencies:
    
    ```sh
    pip install -r requirements.txt
    ```
    

## Usage

Run the following command to start the game:

```sh
python calculate_score.py
```

## How It Works

1. The model detects hand gestures (rock, paper, or scissors) from the webcam.
2. If both players hold their gestures steady for 3 seconds, the game determines the winner.
3. Scores are updated accordingly.
4. The winner's choice is highlighted in green.
