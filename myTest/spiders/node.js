const fs = require('fs')
console.log(JSON.parse(fs.readFileSync('test.json'))[0].movieName)