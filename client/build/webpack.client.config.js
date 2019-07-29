const base = require('./webpack.base.config')
const webpack = require('webpack')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const config = Object.assign({}, base, {
  plugins: base.plugins || []
});

config.plugins.push(
  new MiniCssExtractPlugin({
    filename: 'css/[name].bundle.css'
  })
)

if (process.env.NODE_ENV === 'production') {
  config.plugins.push(
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false
      }
    })
  )
}

module.exports = config
