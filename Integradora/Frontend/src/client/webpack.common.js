
const path = require('path')

module.exports = {
    entry: './src/client/client.ts', // The entry point of the app
    module: {
        rules: [ // Rules for the webpack loader
            {
                test: /\.tsx?$/, // Regex for .ts and .tsx files (TypeScript)
                use: 'ts-loader', // Use the ts-loader to compile the TypeScript
                exclude: /node_modules/, // Exclude node_modules from the loader
            },
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'], // Resolve .ts and .tsx files as well as .js files
    },
    output: {
        filename: 'bundle.js', // The output file name of the bundle
        path: path.resolve(__dirname, '../../dist/client'), // The output path of the bundle
    },
}