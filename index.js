const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let score = 0;
let hscore = 0;
let backgroundX = 0;
let treeX = 550;
let dinoY = 210;
let speed = 5;
const yDef = 6;
let jump = false;
let jumpCount = 0;
const maxJumps = 2;
let lives = 3;
let gameplay = false;
let menu = true;
let heartVisible = false;
let heartX, heartY;

const background = new Image();
background.src = 'assets/resizedBackground.png';
const tree = new Image();
tree.src = 'assets/fire2.png';
const dino = new Image();
dino.src = 'assets/resizedDP.png';
const heart = new Image();
heart.src = 'assets/heart_resized.png';

document.addEventListener('keydown', event => {
    if (menu) {
        if (event.key === '1') {
            speed = 3;
            gameplay = true;
            menu = false;
        }
        if (event.key === '2') {
            speed = 7;
            gameplay = true;
            menu = false;
        }
    }
    if (event.key === ' ' && gameplay) {
        if (jumpCount < maxJumps) {
            jump = true;
            jumpCount += 1;
        }
    }
    if (event.key === ' ' && !gameplay && !menu) {
        resetGame();
    }
});

function resetGame() {
    backgroundX = 0;
    treeX = 550;
    dinoY = 210;
    score = 0;
    lives = 3;
    heartVisible = false;
    gameplay = false;
    menu = true;
    speed = 5;
}

function appearHeart() {
    if (!heartVisible && Math.random() < 0.01) {
        heartX = Math.floor(Math.random() * (1200 - 600 + 1)) + 600;
        heartY = Math.floor(Math.random() * (210 - 80 + 1)) + 80;
        heartVisible = true;
    }
}

function checkCollision(rect1, rect2) {
    return !(
        rect2.left > rect1.right ||
        rect2.right < rect1.left ||
        rect2.top > rect1.bottom ||
        rect2.bottom < rect1.top
    );
}

function update() {
    if (menu) {
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#000';
        ctx.font = '20px Arial';
        ctx.fillText('Dino Game', 250, 50);
        ctx.fillText('Press 1 for Easy', 200, 150);
        ctx.fillText('Press 2 for Hard', 200, 200);
    } else if (gameplay) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        backgroundX -= speed;
        if (backgroundX <= -600) {
            backgroundX = 0;
        }

        ctx.drawImage(background, backgroundX, 0);
        ctx.drawImage(background, backgroundX + 600, 0);

        treeX -= speed;
        if (treeX <= -20) {
            treeX = 550;
        }

        ctx.drawImage(tree, treeX, 230);

        if (dinoY >= 80 && jump) {
            dinoY -= yDef;
        } else {
            jump = false;
        }
        if (dinoY < 210 && !jump) {
            dinoY += yDef;
        }
        if (dinoY === 210) {
            jumpCount = 0;
        }

        ctx.drawImage(dino, 0, dinoY);

        appearHeart();
        if (heartVisible) {
            ctx.drawImage(heart, heartX, heartY);
            heartX -= speed;
            if (heartX < -20) {
                heartVisible = false;
            }
        }

        score += 0.01;
        if (hscore < score) {
            hscore = score;
        }

        const dinoRect = {
            left: 0,
            right: dino.width,
            top: dinoY,
            bottom: dinoY + dino.height,
        };
        const treeRect = {
            left: treeX,
            right: treeX + tree.width,
            top: 230,
            bottom: 230 + tree.height,
        };
        const heartRect = {
            left: heartX,
            right: heartX + heart.width,
            top: heartY,
            bottom: heartY + heart.height,
        };

        if (checkCollision(dinoRect, treeRect)) {
            lives -= 1;
            treeX = 550;
        }

        if (heartVisible && checkCollision(dinoRect, heartRect)) {
            lives += 1;
            heartVisible = false;
        }

        if (lives === 0) {
            gameplay = false;
        }

        ctx.fillStyle = '#f00';
        ctx.font = '20px Arial';
        ctx.fillText(`Score: ${Math.floor(score)}`, 250, 50);
        ctx.fillText(`High Score: ${Math.floor(hscore)}`, 350, 50);
        ctx.fillText(`Lives: ${lives}`, 150, 50);
    } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(background, backgroundX, 0);
        ctx.drawImage(tree, treeX, 230);
        ctx.drawImage(dino, 0, dinoY);
        ctx.fillStyle = '#f00';
        ctx.font = '20px Arial';
        ctx.fillText(`Score: ${Math.floor(score)}`, 250, 50);
        ctx.fillText(`High Score: ${Math.floor(hscore)}`, 350, 50);
        ctx.fillText('Game Over', 250, 210);
        ctx.fillText(`Lives: ${lives}`, 150, 50);
    }

    requestAnimationFrame(update);
}

update();
