module.exports = {
  lintOnSave: true,
  filenameHashing: true,
  productionSourceMap: false,

  css: {
    sourceMap: false,
  },

  chainWebpack: (config) => {
    config.module.rules.delete("svg");
  },
  configureWebpack: {
    performance: {
      hints: false,
    },
    module: {
      rules: [
        {
          test: /\.svg$/,
          loader: "vue-svg-loader",
        },
      ],
    },
  },

  transpileDependencies: ["vuetify"],
};
