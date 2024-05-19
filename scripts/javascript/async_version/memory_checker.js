const axios = require('axios');

async function fetchData() {
    const numRequests = 100;
    const memoryUsageBefore = process.memoryUsage().heapUsed;

    const requests = [];
    for (let i = 0; i < numRequests; i++) {
        const request = axios.get('https://habr.com').catch(error => {
            return null;
        });
        requests.push(request);
    }

    await Promise.all(requests);

    const memoryUsageAfter = process.memoryUsage().heapUsed;
    const memoryUsed = (memoryUsageAfter - memoryUsageBefore) / 1024 / 1024

    console.log(`Использовано памяти: ${memoryUsed} МБ`);
}

fetchData();
