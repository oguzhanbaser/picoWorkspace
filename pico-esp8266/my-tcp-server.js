var net = require('net');

var tcpServer = net.createServer(function (socket) {
    console.log("Client Connected!");
    // socket.write('Echo server\r\n');
    // socket.pipe(socket);
    socket.on('data', function (data) {
        console.log("Rec Data: " + data)
    })

    socket.on('close', function (data) {
        console.log('Client Disconnect')
        clearInterval(sendInterval);
    })

    var led1 = 0;
    var led2 = 1;
    sendInterval = setInterval(function () {
        sendJSON = {"LED1": led1.toString(), "LED2": led2.toString()}
        // socket.write("LED1=" + led1.toString() + ";LED2=" + led2.toString() + ";");
        socket.write("|" + JSON.stringify(sendJSON) + "|");
        led1 = led1 == 0 ? 1 : 0;
        led2 = led2 == 0 ? 1 : 0;
        // console.log("send");
    }, 1000);

});

tcpServer.listen(1337, '192.168.2.135', function () {
    console.log("TCP Server Ready");
});