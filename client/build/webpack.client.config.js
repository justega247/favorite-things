const base = require('./webpack.base.config')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const config = Object.assign({}, base, {
  plugins: base.plugins || []
});

config.plugins.push(
  new MiniCssExtractPlugin({
    filename: 'css/[name].bundle.css'
  })
)

module.exports = config
