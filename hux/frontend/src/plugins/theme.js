import colors from "./colors"

export default {
  primary: {
    lighten1: colors.backgroundBlue,
    lighten2: colors.aliceBlue,
    lighten3: colors.greyBlue,
    lighten4: colors.dullBlue,
    lighten5: colors.columbiaBlue,
    lighten6: colors.skyBlue,
    lighten7: colors.oceanBlue,
    lighten8: colors.blue,
    base: colors.darkBlue,
    darken1: colors.royalBlue,
    darken2: colors.lightBlue,
    darken3: colors.pantoneBlue,
    darken4: colors.tealBlue,
  },
  white: {
    base: colors.white,
  },  
  // pending
  black: {
    lighten1: colors.appBodyGrey,
    lighten2: colors.smoke,
    lighten3: colors.lightGrey,
    lighten4: colors.lightGreyAnotherVariant, 
    base: colors.black, 
    darken1: colors.gray,
    darken2: colors.darkGreyHeading,
    darken3: colors.darkGrey,
    darken4: colors.neroBlack,
  },
  // Here below colors are standard & unique, there is no matching shades between in/any other color palette. 
  error: colors.red,
  success: colors.green,
  warning: colors.yellow,
  zircon: colors.zircon,
  pinkLittleDark: colors.pinkLittleDark,
  persianGreen: colors.persianGreen,
  cerulean: colors.cerulean,
}
