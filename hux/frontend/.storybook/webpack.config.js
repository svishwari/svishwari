const path = require("path")
const VuetifyLoaderPlugin = require("vuetify-loader/lib/plugin")

module.exports = async ({ config }) => {
  config.resolve.extensions.push(".vue", ".css", ".scss", ".sass", ".html")
  config.module.rules.push({
    resourceQuery: /module/,
    use: [
      {
        loader: "vue-style-loader",
        options: {
          sourceMap: false,
          shadowMode: false,
        },
      },
      {
        loader: "css-loader",
        options: {
          sourceMap: false,
          importLoaders: 2,
          modules: true,
          localIdentName: "[name]_[local]_[hash:base64:5]",
        },
      },
      {
        loader: "postcss-loader",
        options: {
          sourceMap: false,
        },
      },
      {
        loader: "sass-loader",
        options: {
          sourceMap: false,
          indentedSyntax: true,
          data: '@import "@/styles/variables.scss";',
        },
      },
    ],
  })
  return config
}
