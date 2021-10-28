module.exports = {
  devServer: {
    disableHostCheck: true, // enabled for: host.docker.internal
  },

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
        {
          test: /\.txt$/,
          use: "raw-loader",
        },
      ],
    },
  },

  css: {
    sourceMap: false,
  },

  chainWebpack: (config) => {
    config.module.rules.delete("svg")

    if (
      process.env.NODE_ENV === "production" &&
      process.env.MIRAGE_ENABLED !== "true"
    ) {
      config.module
        .rule("exclude-mirage")
        .test(/node_modules\/miragejs\//)
        .use("null-loader")
        .loader("null-loader")
    }
  },

  transpileDependencies: ["vuetify"],
}
