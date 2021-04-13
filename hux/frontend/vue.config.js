const CompressionPlugin = require("compression-webpack-plugin");

module.exports = {
  lintOnSave: true,
  filenameHashing: true,
  productionSourceMap: false,

  configureWebpack: {
    performance: {
      hints: false,
    },
  },

  css: {
    sourceMap: false,
  },

  chainWebpack(config) {
    config.plugins.delete("prefetch");

    // and this line
    config.plugin("CompressionPlugin").use(CompressionPlugin);
    const svgRule = config.module.rule("svg");

    svgRule.uses.clear();

    svgRule
      .oneOf("inline")
      .resourceQuery(/inline/)
      .use("vue-svg-loader")
      .loader("vue-svg-loader")
      .end()
      .end()
      .oneOf("external")
      .use("file-loader")
      .loader("file-loader")
      .options({
        name: "assets/[name].[hash:8].[ext]",
      });
  },

  transpileDependencies: ["vuetify"],
};
