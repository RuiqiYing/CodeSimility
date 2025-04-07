const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');  // 自动生成 HTML 文件并注入打包的资源
const MiniCssExtractPlugin = require('mini-css-extract-plugin');  // 提取 CSS
const TerserPlugin = require('terser-webpack-plugin');  // 用于生产环境下压缩 JavaScript

module.exports = {
  // 入口文件
  entry: './src/index.js',  // 你的应用入口文件

  // 输出文件配置
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',  // 打包后的文件名
  },

  // 配置加载器
  module: {
    rules: [
      {
        test: /\.js$/,  // 处理 JavaScript 文件
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],  // 使用 Babel 进行 JavaScript 转译
          },
        },
      },
      {
        test: /\.css$/,  // 处理 CSS 文件
        use: [
          MiniCssExtractPlugin.loader,  // 提取 CSS 为独立文件
          'css-loader',  // 解析 CSS 文件
        ],
      },
      {
        test: /\.(png|jpg|gif|svg)$/,  // 处理图片文件
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 8192,  // 8KB 以下的图片会转为 Base64 格式
            },
          },
        ],
      },
    ],
  },

  // 配置插件
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',  // 自动生成的 HTML 文件模板
    }),
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css',  // 输出的 CSS 文件名
    }),
  ],

  // 优化配置
  optimization: {
    splitChunks: {
      chunks: 'all',  // 分割所有类型的模块
    },
    minimize: true,  // 启用压缩
    minimizer: [
      new TerserPlugin(),  // 生产环境下压缩 JavaScript 代码
    ],
  },

  // 配置开发服务器
  devServer: {
    contentBase: path.resolve(__dirname, 'dist'),
    port: 9000,  // 开发服务器运行的端口
    hot: true,  // 启用热更新
    open: true,  // 启动后自动打开浏览器
  },

  // 配置源映射（用于调试）
  devtool: 'source-map',  // 在开发时使用 'source-map' 生成源映射

  // 设置开发和生产环境
  mode: 'development',  // 设置开发模式，生产环境可以设置为 'production'
};
