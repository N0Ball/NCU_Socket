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
    }

    json(){
        return this.json;
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

function decodeUtf8(s) {
    return decodeURIComponent(escape(s));
  }