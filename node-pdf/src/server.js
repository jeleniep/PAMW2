import express from 'express';
import multer from 'multer';
import bodyParser from 'body-parser';
import jwt from 'jsonwebtoken';
import fs from 'fs';
import { promisify } from 'util'
const PORT = 8080;
const HOST = '0.0.0.0';
const KEY = 'secret'


const app = express();
const storage = multer.diskStorage(
  {
      destination: './uploads/',
      filename: function ( req, file, cb ) {
          cb( null, file.fieldname );
      }
  }
);
const multerupload = multer({ 
  storage
})
const router = express.Router();

const readdirp = promisify(fs.readdir);

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const verifyToken = (req, res, next) => { 
  if (!jwt.verify(req.headers.authorization, KEY)) {
    res.status(401).send();
  }
  next();
}

const verifyTokenParam = (req, res, next) => {
  if (!jwt.verify(req.query.token, KEY)) {
    res.status(401).send();
  }
  next();
}


const getPdf = (req, res) => {
  const file = `${__dirname}/../uploads/${req.params.name}`;
  res.download(file);
}

const getPdfList = async (req, res) => {
  const files = await readdirp(`${__dirname}/../uploads`);
  res.json(files);
}

router.post('/addPdf', verifyToken, multerupload.any());
router.get('/getPdf/:name', verifyTokenParam, getPdf);
router.get('/getPdfList', verifyToken, getPdfList);


app.use('/', router);
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);