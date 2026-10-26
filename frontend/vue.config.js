module.exports = {
  devServer: {
    historyApiFallback: true,
    hot: true,
    port: 8080,
    host: "localhost",
    allowedHosts: "all",
  },

  publicPath: "/",

  lintOnSave: false,

  configureWebpack: {
    devtool: "source-map",
  },

  productionSourceMap: false,

  css: {
    extract: process.env.NODE_ENV === "production",
    sourceMap: true,
  },
};
