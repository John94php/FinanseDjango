//const { defineConfig } = require('@vue/cli-service')
//module.exports = defineConfig({
//  transpileDependencies: true
//})

const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, '../static'), // ścieżka do katalogu 'static' Django
  indexPath: '../templates/index.html', // ścieżka do katalogu 'templates' Django
  // ...
}
