// Needed to load customizations made in variables.scss for vuetify
// See: https://vuetifyjs.com/en/features/treeshaking/#webpack-installation
const VuetifyLoaderPlugin = require("vuetify-loader/lib/plugin")

module.exports = {
  stories: ["../src/**/*.stories.js"],

  addons: ["@storybook/addon-essentials"],

  webpackFinal: async (config) => {
    config.plugins.push(new VuetifyLoaderPlugin())

    return config
  },
}
