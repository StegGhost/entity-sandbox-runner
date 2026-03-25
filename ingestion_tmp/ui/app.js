
async function fetchData() {
    return {
        metrics: { success: 10, failure: 2, failure_rate: 0.16 },
        state: { system: "running" },
        events: ["event1", "event2"]
    };
}

async function refresh() {
    const data = await fetchData();
    document.getElementById("metrics").innerText = JSON.stringify(data.metrics, null, 2);
    document.getElementById("state").innerText = JSON.stringify(data.state, null, 2);
    document.getElementById("events").innerText = JSON.stringify(data.events, null, 2);
}

refresh();
