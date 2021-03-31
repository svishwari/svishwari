import { createMuiTheme } from '@material-ui/core/styles';

const theme = createMuiTheme({
  typography: {
    fontFamily: 'Open Sans SemiBold',
    letterSpacing: 0.1,
    color: '#333333',
    fontStyle: 'normal',
    fontWeight: 600,
  },
  boldFont: 'Open Sans SemiBold',
  colors: {
    primary: {},
    secondary: {
        green: '#43B02A',
        white: "#FFFFFF"
    },
  },
  props: {
    // Name of the component
    MuiButtonBase: {
      // The properties to apply
      disableRipple: true // No more ripple, on the whole application!
    }
  }
});

export default theme;
