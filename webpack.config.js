// Not part of the project, but used for CI/CD
const path = require('path');

module.exports = {
  entry: './components/global-header.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
  },
  mode: 'production',
};
