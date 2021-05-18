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
}
