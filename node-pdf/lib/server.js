'use strict';

var _express = require('express');

var _express2 = _interopRequireDefault(_express);

var _multer = require('multer');

var _multer2 = _interopRequireDefault(_multer);

var _bodyParser = require('body-parser');

var _bodyParser2 = _interopRequireDefault(_bodyParser);

var _jsonwebtoken = require('jsonwebtoken');

var _jsonwebtoken2 = _interopRequireDefault(_jsonwebtoken);

var _fs = require('fs');

var _fs2 = _interopRequireDefault(_fs);

var _util = require('util');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var PORT = 8081;
var HOST = '0.0.0.0';
var KEY = 'secret';

var app = (0, _express2.default)();
var storage = _multer2.default.diskStorage({
  destination: './uploads/',
  filename: function filename(req, file, cb) {
    cb(null, file.fieldname);
  }
});
var multerupload = (0, _multer2.default)({
  storage: storage
});
var router = _express2.default.Router();

var readdirp = (0, _util.promisify)(_fs2.default.readdir);

app.use(_bodyParser2.default.urlencoded({ extended: true }));
app.use(_bodyParser2.default.json());

var verifyToken = function verifyToken(req, res, next) {
  if (!_jsonwebtoken2.default.verify(req.headers.authorization, KEY)) {
    console.log("test");
    res.status(401).send();
  }
  console.log(req.headers);
  req.xdd = "hahga";
  next();
};

var verifyTokenParam = function verifyTokenParam(req, res, next) {
  console.log(req.query);
  if (!_jsonwebtoken2.default.verify(req.query.token, KEY)) {
    console.log("test");
    res.status(401).send();
  }
  req.xdd = "hahga";
  next();
};

var addPdf = function addPdf(req, res) {
  console.log(req.files);
  console.log(_jsonwebtoken2.default.verify(req.headers.authorization, KEY));
  res.status(500).send('Nice');
};

var getPdf = function getPdf(req, res) {
  console.log(req.headers);
  var file = __dirname + '/../uploads/' + req.params.name;
  res.download(file);
};

var getPdfList = async function getPdfList(req, res) {
  var files = await readdirp(__dirname + '/../uploads');
  res.json(files);
};

router.post('/addPdf', verifyToken, multerupload.any(), addPdf);
router.get('/getPdf/:name', verifyTokenParam, getPdf);
router.get('/getPdfList', verifyToken, getPdfList);

app.use('/', router);
app.listen(PORT, HOST);
console.log('Running on http://' + HOST + ':' + PORT);