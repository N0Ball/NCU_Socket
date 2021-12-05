const OFFSET = 30;
const VELOCITY = 80;
const FONTFAMILY = 'Allerta Stencil';
const COLORS = ['LightGreen', 'LightPink', 'LightBlue', 'DarkSeaGreen', 'GoldenRod', 'Violet'];

class Position{
    constructor(x, y){
        this.x = x;
        this.y = y;
    }
}

class Text{
    constructor(text, ctx, x, y){
        this.text = text;
        this.ctx = ctx;
        this.originX = x;
        this.position = new Position(x, y);
        this.velocity = -VELOCITY;
        this.dt = 0.01;
        this.w = this.ctx.measureText(this.text).width;
        this.color = COLORS[Math.floor(COLORS.length*Math.random())]
    }

    move(){
        this.position.x += this.velocity * this.dt;
    }

    checkEmpty(){
        return this.position.x > (this.originX - this.w - OFFSET) ? this.position.y/OFFSET : 0
    }

    update(){
        this.move();
        this.ctx.fillStyle = this.color;
        this.ctx.fillText(this.text, this.position.x, this.position.y);
    }
}

class TextManager{
    constructor(canvas){
        this.canvas = canvas;
        this.canvas.style = `
            position: absolute;
            background-color: rgba(0, 0, 0, 0.11);
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            z-index: 99999;
            top: 0;
            left: 0;
            pointer-events: none;
        `;
        this.ctx = canvas.getContext('2d');
        this.ctx.font = `normal 36px ${FONTFAMILY}, monospace`;
        this.ctx.fillstyle = 'cornflowerblue';
        this.ctx.textAlign = 'start';
        this.TEXTS = [];
    };

    addText(text){
        let emptyList = new Array(1e3);
        let max = 0;

        emptyList[0] = false;
        for (let text of this.TEXTS){
            max = Math.max(max, text.checkEmpty());
            emptyList[text.checkEmpty()] = false;
        }

        if(this.TEXTS.length == 0){
            this.TEXTS.push(new Text(text, this.ctx, this.canvas.width, OFFSET));
            return;
        }

        for (let i = 0; i < emptyList.length; i++){

            if (emptyList[i] == undefined){
                if (max == i){
                    this.TEXTS.push(new Text(text, this.ctx, this.canvas.width, OFFSET*(i + 1)));
                }else{
                    this.TEXTS.push(new Text(text, this.ctx, this.canvas.width, OFFSET*(i)));
                }
                break;
            }
        }

    }

    update(){

        this.ctx.clearRect(0, 0, 2*window.innerHeight, 2*window.innerWidth);

        for(let i = 0; i < this.TEXTS.length; i++){
            let text = this.TEXTS[i];
            text.update();

            if(text.position.x < -text.w){
                this.TEXTS.splice(i, 1);
            }
        }

    }
}