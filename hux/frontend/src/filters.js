/**
 * Globally registerd Vue filters
 */
import moment from "moment"

export default {
  /**
   * Formats a datetime field to human friendly date.
   *
   * @param {*} value Datetime eg. 2021-03-17T23:29:49.351Z
   * @param {*} format Format eg. "MM/D/YYYY [at] hh:ss A"
   * @return {string} Formatted date time string eg. 17/3/2021 at 11:29pm
   */
  Date(value, format = "MM/D/YYYY [at] hh:ss A") {
    if (!value) return ""

    if (format === "relative") return moment(value).fromNow()

    if (format === "calendar") return moment(value).calendar()

    return moment(value).format(format)
  },

  /**
   * Formats any empty data field with a placeholder.
   *
   * @param {*} value Empty string eg. ""
   * @param {*} placeholder Placeholder eg. "N/A"
   * @returns Formatted empty data field eg. "N/A"
   */
  Empty(value, placeholder = "—") {
    if (!value) return placeholder
    return value
  },

  Numeric(
    value,
    round = false,
    abbreviate = false,
    approx = false,
    append = ""
  ) {
    if (isNaN(value)) return ""

    let abrv = ""

    if (abbreviate) {
      if (value >= 1000000) {
        value = value / 1000000
        abrv = "m"
      } else if (value >= 1000) {
        value = value / 1000
        abrv = "k"
      }
    }
    if (approx) {
      // Nine Zeroes for Billions
      value =
        Math.abs(Number(value)) >= 1.0e9
          ? (Math.abs(Number(value)) / 1.0e9).toFixed(1) + "B"
          : // Six Zeroes for Millions
          Math.abs(Number(value)) >= 1.0e6
          ? (Math.abs(Number(value)) / 1.0e6).toFixed(1) + "M"
          : // Three Zeroes for Thousands
          Math.abs(Number(value)) >= 1.0e3
          ? (Math.abs(Number(value)) / 1.0e3).toFixed(1) + "K"
          : Math.abs(Number(value))
    }

    return approx
      ? value
      : value.toLocaleString("en-US", {
          minimumFractionDigits: 0,
          maximumFractionDigits: round && Number(value) ? 0 : 2,
        }) +
          abrv +
          append
  },

  /**
   * Formats a string with title case.
   *
   * @param {*} value The string eg. "active Customers"
   * @returns Title cased string eg. "Active Customers"
   */
  TitleCase(value) {
    return value.replace(/\w\S*/g, function (txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
    })
  },
  /**
   * Formats any string(fullname) to shortname.
   *
   * @param {*} value The string eg. "John petro"
   * @returns shortname string eg. "JP"
   */
  shortName(value) {
    return value
      .split(" ")
      .map((n) => n[0])
      .join("")
  },
  Currency(value) {
    return Number(value).toLocaleString("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    })
  },
}
