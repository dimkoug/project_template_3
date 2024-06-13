const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: {
        main: './static/js/index.js',
    },
    output: {
        path: path.resolve(__dirname, 'static/dist'),
        filename: '[name].bundle.js',
        publicPath: '/static/dist/',
    },
    plugins: [
        new BundleTracker({ filename: 'webpack-stats.json' }),
        new MiniCssExtractPlugin({
            filename: '[name].bundle.css',
        }),
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                    },
                },
            },
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader'],
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]',
                            outputPath: 'images/',
                        },
                    },
                ],
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.css'],
    },
    devServer: {
        static: {
            directory: path.resolve(__dirname, 'static/dist'),
        },
        compress: true,
        port: 9000,
        hot: true,
        devMiddleware: {
            publicPath: '/static/dist/',
        },
        watchFiles: ['static/js/**/*', 'static/css/**/*'],
    },
};
