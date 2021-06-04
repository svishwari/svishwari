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

  Numeric(value, round = false, abbreviate = false, append = "") {
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

    return (
      value.toLocaleString("en-US", {
        minimumFractionDigits: 0,
        maximumFractionDigits: round && Number(value) ? 0 : 2,
      }) +
      abrv +
      append
    )
  },

  /**
   * Formats a string with title case.
   *
   * @param {*} value The string eg. "active Customers"
   * @returns Title cased string eg. "Active Customers"
   */
  TitleCase(value) {
    return value
      .replace(/([A-Z])/g, (match) => ` ${match}`)
      .replace(/^./, (match) => match.toUpperCase())
      .trim()
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
  /**
   * Format the number with comma
   *
   * @param {*} value the number eg "125767"
   * @returns formatted number
   */
  FormatSize(value) {
    return Number(value).toLocaleString()
  },
}
