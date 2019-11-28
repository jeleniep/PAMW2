'use strict';

var _express = require('express');

var _express2 = _interopRequireDefault(_express);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// Constants
var PORT = 8081;
var HOST = '0.0.0.0';

// App
var app = (0, _express2.default)();
app.get('/', function (req, res) {
  res.send('Hello world\n');
});

app.listen(PORT, HOST);
console.log('Running on http://' + HOST + ':' + PORT);