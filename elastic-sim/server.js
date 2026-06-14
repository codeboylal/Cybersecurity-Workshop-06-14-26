const http = require('http');

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('X-elastic-product', 'Elasticsearch');

  const url = req.url || '/';

  if (url === '/' || url === '') {
    res.end(JSON.stringify({
      name: 'es-node-1',
      cluster_name: 'innovatetech-cluster',
      cluster_uuid: 'abc123def456',
      version: { number: '7.17.0', build_flavor: 'default', lucene_version: '8.11.1' },
      tagline: 'You Know, for Search'
    }));
  } else if (url.includes('_cat/indices')) {
    res.end(JSON.stringify([
      { index: 'employees', 'docs.count': '1500', 'store.size': '2.3mb', status: 'green' },
      { index: 'customers', 'docs.count': '8200', 'store.size': '12mb', status: 'green' },
      { index: 'internal-secrets', 'docs.count': '3', 'store.size': '4kb', status: 'yellow' },
      { index: 'audit-logs', 'docs.count': '45000', 'store.size': '89mb', status: 'green' }
    ]));
  } else if (url.includes('internal-secrets/_search') || url.includes('internal-secrets/_doc')) {
    res.end(JSON.stringify({
      hits: {
        total: { value: 3, relation: 'eq' },
        hits: [
          {
            _index: 'internal-secrets',
            _id: '1',
            _source: {
              flag: 'FLAG{3l4st1c_n0_4uth_1nd3x_3xp0s3d}',
              data: 'employee_ssn,salary_data,api_keys',
              severity: 'CRITICAL',
              note: 'This index should NOT be public!'
            }
          },
          {
            _index: 'internal-secrets',
            _id: '2',
            _source: { type: 'api_key', key: 'sk-prod-7f3k9x2mAbCdEf123456', service: 'main-api' }
          },
          {
            _index: 'internal-secrets',
            _id: '3',
            _source: { type: 'db_password', host: 'mysql', user: 'root', password: 'root' }
          }
        ]
      }
    }));
  } else if (url.includes('employees/_search')) {
    res.end(JSON.stringify({
      hits: {
        total: { value: 1500 },
        hits: [
          { _source: { name: 'John Doe', salary: 95000, ssn: '123-45-6789', email: 'john@innovatetech.com' } },
          { _source: { name: 'Jane Smith', salary: 120000, ssn: '987-65-4321', email: 'jane@innovatetech.com' } }
        ]
      }
    }));
  } else {
    res.statusCode = 404;
    res.end(JSON.stringify({ error: { reason: 'no such index', type: 'index_not_found_exception' } }));
  }
});

server.listen(9200, '0.0.0.0', () => {
  console.log('Elasticsearch simulator running on port 9200');
});
