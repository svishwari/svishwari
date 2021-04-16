module.exports = {
  lintOnSave: process.env.NODE_ENV !== "production",
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
    config.module.rules.delete("svg")
  },

  transpileDependencies: ["vuetify"],
}
