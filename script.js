async function updateServer() {
    try {
        const res = await fetch(
            "https://servers-frontend.fivem.net/api/servers/single/yoo56k"
        );

        const json = await res.json();

        document.getElementById("players").innerText =
            `${json.Data.clients}/${json.Data.sv_maxclients}`;

        document.getElementById("servername").innerText =
            json.Data.hostname;
    } catch (err) {
        console.log(err);
    }
}

updateServer();
setInterval(updateServer, 30000);
