const request = require('sync-request');

function fetchSync(url) {
    try {
        const response = request('GET', url);
        return response.statusCode;
    } catch (error) {
        return null;
    }
}

function fetchData() {
    const url = 'https://habr.com';
    const numRequests = 100;
    const memoryUsageBefore = process.memoryUsage().heapUsed;

    for (let i = 0; i < numRequests; i++) {
        fetchSync(url);
    }

    const memoryUsageAfter = process.memoryUsage().heapUsed;
    const memoryUsed = (memoryUsageAfter - memoryUsageBefore) / 1024 / 1024

    console.log(`Использовано памяти: ${memoryUsed} МБ`);
}

fetchData();
