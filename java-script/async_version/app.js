const http = require('http');
const Processor = require('./Processor');

const port = process.env.PORT || 9001;

http.createServer((request, response) => {
  const parsedUrl = require('url').parse(request.url, true);

  // Используем console.time для начала отсчета времени
  console.time('Request Processing Time');

  if (parsedUrl.pathname === '/getSubsets') {
    const inputData = JSON.parse(parsedUrl.query.data);
    response.writeHead(200);

    const SubsetProcessor = new Processor(parsedUrl.query.sum, inputData);
    SubsetProcessor.on('end', () => {
      // Используем console.timeEnd для окончания отсчета времени
      console.timeEnd('Request Processing Time');
      response.end(JSON.stringify(SubsetProcessor.matchCount) + '\n');
    });
    
    SubsetProcessor.initiate();
  } else {
    response.writeHead(200);
    response.end("Successful!\n");

    // В случае других эндпоинтов также используем console.timeEnd
    console.timeEnd('Request Processing Time');
  }
}).listen(port, () => console.log('Started server on port ' + port));