var path = require('path');
var webpack = require('webpack');

module.exports = {
  entry: ['whatwg-fetch', './static/js/profile.js', './static/js/tariff.js', './static/js/payments.js'],
  output: { path: __dirname+'/static/js/', filename: 'bundle.js' },
  module: {
    loaders: [
      {
        test: /.jsx?$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          presets: ['es2015', 'react']
        }
      }
    ]
  },
};
