import colors from "./colors"

export default {
  // New Design System
  primary: {
    lighten1: colors.backgroundLight,
    lighten2: colors.backgroundMed,
    lighten3: colors.pills,
    lighten4: colors.lightBlueD,
    lighten5: colors.chart4,
    lighten6: colors.blueD,
    // TODO Remove the below after a couple of sprints
    lighten7: colors.oceanBlue,
    lighten8: colors.blue,
    // TODO Ends here
    lighten9: colors.chart3,
    base: colors.chart2,
    darken1: colors.medBlueD,
    darken2: colors.darkBlue,
    darken3: colors.blue,
    // TODO Remove the below after a couple of sprints
    darken4: colors.tealBlue,
    // TODO Ends here
  },
  black: {
    lighten1: colors.inactiveButton,
    lighten2: colors.borderBase,
    lighten3: colors.linesHeavy,
    lighten4: colors.lightGray,
    base: colors.darkD,
    // TODO Remove the below after a couple of sprints
    darken1: colors.gray,
    darken2: colors.darkGreyHeading,
    darken3: colors.darkGrey,
    darken4: colors.neroBlack,
    // TODO Ends here
  },
  teal: {
    lighten1: colors.lightTealD,
    lighten2: colors.tealD,
    lighten3: colors.lightGreenD,
    base: colors.greenD,
    darken2: colors.teal6D,
    darken3: colors.teal7D,
  },
  yellow: {
    lighten1: colors.yellow5,
    base: colors.yellow,
    darken1: colors.mustard,
  },
  warning: colors.warning,
  white: {
    base: colors.white,
  },
  error: colors.error,

  // Old Design System

  // Here below colors are standard & unique, there is no matching shades between in/any other color palette.
  success: colors.green,
  zircon: colors.zircon,
  pinkLittleDark: colors.pinkLittleDark,
  persianGreen: colors.persianGreen,
  cerulean: colors.cerulean,
}
