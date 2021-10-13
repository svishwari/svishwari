// Needed to load customizations made in variables.scss for vuetify
// See: https://vuetifyjs.com/en/features/treeshaking/#webpack-installation
const VuetifyLoaderPlugin = require("vuetify-loader/lib/plugin")

module.exports = {
  stories: ["../src/**/*.stories.mdx", "../src/**/*.stories.@(js|jsx|ts|tsx)"],

  addons: ["@storybook/addon-essentials", "@storybook/addon-docs"],

  webpackFinal: async (config) => {
    config.plugins.push(new VuetifyLoaderPlugin())

    return config
  },
}
