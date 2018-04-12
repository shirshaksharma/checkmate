# Check Mate
Python application that uses Computer Vision so you can play chess using only a piece of paper.

### Pre-requisites
- **Python**: You will need Python 3 installed on your machine.
- **Webcam**: You will need either a laptop webcam or an external camera to detect the chessboard.
- **Chessboard**: You can print out [this](board.jpg) chessboard on a regular sheet of paper for
Checkmate to scan.

### Installation

```
$ git clone https://github.com/shirshaksharma/checkmate
$ cd checkmate
$ pip3 install -r requirements.txt
```
### Starting the game

```
$ python3 game.py
```

The application will ask you to choose a camera to use.
Press `0` if you are using the webcam on your computer and `1` if you are using an external camera.

The camera feed and a browser window (with the chessboard)is opened at launch. 
Arrange the windows so you can see both of them easily.

Press `s` to scan the area for the board.

![](https://i.imgur.com/IqVwVSL.jpg)

If you need to flip the image, press `f`.
If you need to rotate the board for easier play, press `r`.

### Game Play

The board will highlight the back row for the current players turn. 
**Player 1 is Red** and **Player 2 is Blue**.


Once you have successfully oriented the board, select a piece by placing your finger on the square that that piece 
is in.
The square, once selected, will be outlined in **Red**. 

![](https://i.imgur.com/mX3iIOq.jpg)

The squares that are valid moves for that piece will be 
outlined in **Green**.
![](https://i.imgur.com/TJUl3xA.jpg)

To move the piece to a valid square, place your finger in one of the Green squares. To choose a different piece 
to move, place your finger in the new pieces square.

To undo a move, press `u`.


Once the game is over, the window will close.
To quit the game manually, press `q` while the camera window is selected.
