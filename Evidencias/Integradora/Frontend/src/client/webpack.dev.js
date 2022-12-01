const { merge } = require('webpack-merge') // Import the merge function from webpack-merge
const common = require('./webpack.common.js') // Import the common webpack config
const path = require('path') // Import the path module

module.exports = merge(common, { // Merge the common config with the dev config
    mode: 'development', // Set the mode to development
    devtool: 'eval-source-map', // Set the devtool to eval-source-map
    devServer: { // Set the devServer options
        static: { // Set the static options
            directory: path.join(__dirname, '../../dist/client'), // Set the directory to the dist/client folder
        },
        hot: true, // Enable hot reloading
    },
})