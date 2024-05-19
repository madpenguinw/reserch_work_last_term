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
    const startTime = Date.now();

    for (let i = 0; i < numRequests; i++) {
        fetchSync(url);
    }

    const endTime = Date.now();
    const executionTime = (endTime - startTime) / 1000;
    console.log(`Время выполнения: ${executionTime} секунд`);
}

fetchData();
