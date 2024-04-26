const http = require('http');
const Processor = require('./Processor');

const port = process.env.PORT || 9000;

http.createServer((request, response) => {
  const parsedUrl = require('url').parse(request.url, true);

  const startTime = Date.now();

  if (parsedUrl.pathname === '/getSubsets') {
    const inputData = JSON.parse(parsedUrl.query.data);
    response.writeHead(200);

    const SubsetProcessor = new Processor(parsedUrl.query.sum, inputData);
    SubsetProcessor.on('end', (matchCount) => {
      const endTime = Date.now();
      const deltaTime = endTime - startTime;
      const responseData = {
        Service: "JavaScript Sync Version",
        Result: matchCount,
        Time: `${deltaTime.toFixed(3)}ms`
      };
      response.end(JSON.stringify(responseData) + '\n');
    });

    SubsetProcessor.initiate();
  } else {
    response.writeHead(200);
    response.end("Successful!\n");
  }
}).listen(port, () => console.log('Started server on port ' + port));
