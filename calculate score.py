import cv2
import time
from ultralytics import YOLO

model = YOLO("best.pt")
classes = ["rock" , "paper" , "scissors"]
cap = cv2.VideoCapture(0)
player1_score = 0
player2_score = 0
stable_choices = []
stable_time = time.time()
countdown_active = False
winner_display_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    roi_x1, roi_y1 = int(w * 0.05) , int(h * 0.15)
    roi_x2, roi_y2 = int(w * 0.95) , int(h * 0.85)

    results = model(frame)
    detections = []

    player1_choice = None
    player2_choice = None
    player1_box = None
    player2_box = None

    for r in results:
        for box in r.boxes:
            x1 , y1 , x2 , y2 = map(int , box.xyxy[0])
            cls_id = int(box.cls[0])
            center_x = (x1 + x2) // 2

            # Check if detection is inside ROI
            if roi_x1 <= center_x <= roi_x2 and roi_y1 <= y2 <= roi_y2:
                detections.append((classes[cls_id] , (x1 , y1 , x2 , y2)))

    # Assign players
    detections.sort(key=lambda d : d[1][0]) 
    if len(detections) >= 2 :
        player1_choice, player1_box = detections[0]
        player2_choice, player2_box = detections[1]

    countdown = 0
    if player1_choice and player2_choice:
        if stable_choices == [player1_choice , player2_choice] :
            if not countdown_active:
                stable_time = time.time()
                countdown_active = True

            elapsed_time = time.time() - stable_time
            countdown = max(0 , 3 - int(elapsed_time))

            if countdown == 0 :
                winner_display_time = time.time()

                if player1_choice == player2_choice:
                    pass
                elif (player1_choice == "rock" and player2_choice == "scissors") or \
                     (player1_choice == "scissors" and player2_choice == "paper") or \
                     (player1_choice == "paper" and player2_choice == "rock"):
                    player1_score += 1
                else:
                    player2_score += 1

                stable_choices = []
                countdown_active = False
        else:
            stable_choices = [player1_choice, player2_choice]
            stable_time = time.time()
            countdown_active = False

    # Draw bounding boxes
    for choice, (x1, y1, x2, y2) in detections:
        color = (255, 255, 255) 

        if countdown_active:
            color = (255, 0, 0)  

        if winner_display_time and time.time() - winner_display_time < 1:
            if choice == player1_choice and player1_score > player2_score:
                color = (0, 255, 0) 
                cv2.putText(frame, "Winner", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif choice == player2_choice and player2_score > player1_score:
                color = (0, 255, 0) 
                cv2.putText(frame, "Winner", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                color = (0, 0, 255)  

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # Score color
    if player1_score > player2_score:
        p1_color = (0, 255, 0)  
        p2_color = (0, 0, 255)  
    elif player2_score > player1_score:
        p1_color = (0, 0, 255)  
        p2_color = (0, 255, 0)  
    else:
        p1_color = p2_color = (255, 255, 255)  

    cv2.putText(frame, f"P1: {player1_score}", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, p1_color, 2)
    cv2.putText(frame, f"P2: {player2_score}", (w - 120, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, p2_color, 2)
    cv2.putText(frame, f"{countdown}", (w // 2 - 20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 255), 1)

    cv2.imshow("Rock Paper Scissors", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
