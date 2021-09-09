import { withVuetify, withThemeProvider } from '@socheatsok78/storybook-addon-vuetify/dist/decorators'

export const globalTypes = {
  theme: {
    name: 'Theme',
    description: 'Global theme for components',
    defaultValue: 'light',
    toolbar: {
      icon: 'circlehollow',
      items: ['light', 'dark']
    }
  }
}

export const decorators = [
  withThemeProvider,
  withVuetify
]