const axios = require('axios');

async function fetchData() {
    const numRequests = 100;
    const startTime = Date.now();

    const requests = [];
    for (let i = 0; i < numRequests; i++) {
        const request = axios.get('https://habr.com').catch(error => {
            return null;
        });
        requests.push(request);
    }

    await Promise.all(requests);

    const endTime = Date.now();
    const executionTime = (endTime - startTime) / 1000;

    console.log(`Время выполнения: ${executionTime} секунд`);
}

fetchData();
