const net = require("net");
const readline = require("readline");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question("Ingrese la IP del servidor: ", (host) => {
  rl.question("Ingrese el puerto del servidor: ", (port) => {
    const client = new net.Socket();

    client.connect(port, host, () => {
      console.log(
        `[SERVER] Conectado exitosamente al servidor en ${host}:${port}
      `);

      rl.question("Ingrese su nombre de usuario: ", (username) => {
        client.write(username);

        rl.on("line", (input) => {
          if (input === "/listar") {
            client.write("/listar");
          } else if (input === "/quitar") {
            client.write("/quitar");
            client.end();
            rl.close();
          } else {
            client.write(input);
          }
        });
      });
    });

    client.on("data", (data) => {
      console.log(data.toString());
    });

    client.on("close", () => {
      console.log("Conexión cerrada");
    });

    client.on("error", (err) => {
      console.error("Error de conexión: ${err.message}");
      rl.close();
    });
  });
});
