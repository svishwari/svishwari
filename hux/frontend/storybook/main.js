// Needed to load customizations made in variables.scss for vuetify
// See: https://vuetifyjs.com/en/features/treeshaking/#webpack-installation
const VuetifyLoaderPlugin = require("vuetify-loader/lib/plugin")

module.exports = {
  stories: ["../src/**/*.stories.@(js|jsx|ts|tsx|mdx)"],

  addons: [
    "@storybook/addon-essentials",
    "storybook-addon-designs",
  ],

  webpackFinal: async (config) => {
    config.plugins.push(new VuetifyLoaderPlugin())

    return config
  },
}
