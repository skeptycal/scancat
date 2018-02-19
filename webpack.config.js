const path = require('path');

module.exports = {
  entry: './static/js/site.js',
  output: {
    filename: 'dist.js',
    path: path.resolve(__dirname, 'static/js/')
  },
  module: {
    rules: [
      { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" }
    ]
  }
};