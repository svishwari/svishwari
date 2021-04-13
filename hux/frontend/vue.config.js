module.exports = {
  lintOnSave: true,
  filenameHashing: true,
  productionSourceMap: false,

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

  css: {
    sourceMap: false,
  },

  chainWebpack: (config) => {
    config.module.rules.delete("svg");
  },

  transpileDependencies: ["vuetify"],
};
