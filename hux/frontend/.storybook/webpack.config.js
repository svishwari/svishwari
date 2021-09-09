const path = require("path")

module.exports = async ({ config }) => {
  config.resolve.alias["~storybook"] = path.resolve(__dirname)

  config.module.rules.push({
    resourceQuery: /blockType=story/,
    loader: "vue-storybook"
  })

  config.module.rules.push({
    test: /\.s(a|c)ss$/,
    use: [
      "vue-style-loader",
      "css-loader",
      {
        loader: "sass-loader",
        options: {
          // additionalData: `@import "${path.resolve(__dirname, "..", "src", "styles", "variables.scss")}"`
        }
      }
    ],
    include: path.resolve(__dirname, "../")
  })

  return config
}
