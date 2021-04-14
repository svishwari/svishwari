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

  chainWebpack: config => {
    config.module.rules.delete("svg");
  },
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.svg$/, 
          loader: 'vue-svg-loader', 
        },
      ],
    }      
  },

  transpileDependencies: ["vuetify"],
};
