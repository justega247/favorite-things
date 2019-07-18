const webpack = require("webpack");
const config = require("./webpack.client.config");
const webpackDevMiddleware = require('webpack-dev-middleware');
const webpackHotMiddleware = require("webpack-hot-middleware")


module.exports = function setupDevServer (app) {
  config.entry.app = [
    "webpack-hot-middleware/client",
    config.entry.app
  ]
  config.plugins.push(
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin()
  );
  const compiler = webpack(config);
  app.use(webpackDevMiddleware(compiler, {
    stats: {
      colors: true
    }
  }));
  app.use(webpackHotMiddleware(compiler));
}
