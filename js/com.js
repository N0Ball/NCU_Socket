class COMSend{
    constructor(op, data){
        this.op = op;
        this.data = data;
    }

    json(){
        return JSON.stringify({
            "OP": this.op,
            "DATA": this.data
        })
    }
}

class COMRecv{
    constructor(json){
        this.json = JSON.parse(json);

        this.operate(this.json);
    }

    operate(json){
        console.log(json);
        let op = json.OP;
        let data = json.DATA;

        if(op == COMOp.MSG){
            pushMsg(data);
        }
    }
}

class COMOp{
    constructor(){
        this.PING = 0x1;
        this.PONG = 0x2;
        this.MSG  = 0x3;
        this.MOVE = 0x4;
    }
}

COMOp = new COMOp();