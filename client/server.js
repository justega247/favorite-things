import express from 'express';
import path from'path';
import fs from 'fs';
import cors from 'cors';
import devServer from './build/dev-server';

const app = express();

app.use(cors())

const indexHTML = (() => {
  return fs.readFileSync(path.resolve(__dirname, './index.html'), 'utf-8')
})()

app.use('/dist', express.static(path.resolve(__dirname, './dist')))

devServer(app);

app.get('*', (req, res) => {
  res.write(indexHTML)
  res.end()
})

const port = process.env.PORT || 3000
app.listen(port, () => {
  console.log(`server started at http://localhost:${port}`)
});
