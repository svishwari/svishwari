/**
 * Globally registered Vue filters
 */
import dayjs from "dayjs"
import calendar from "dayjs/plugin/calendar"
import relativeTime from "dayjs/plugin/relativeTime"
import utc from "dayjs/plugin/utc"
import timezone from "dayjs/plugin/timezone"
import advancedFormat from "dayjs/plugin/advancedFormat"

dayjs.extend(calendar)
dayjs.extend(relativeTime)
dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.extend(advancedFormat)

/**
 * Formats a datetime field to human friendly date.
 *
 * @param {string|*} value Datetime eg. 2021-03-17T13:29:49.351Z
 * @param {string} format Format eg. "MM/D/YYYY [at] hh:ss A"
 * @param {string} local Format eg. true if true, it will use the local time zone if user.
 * @param {boolean} noSuffix Whether to include a suffix
 * @returns {string} Formatted date time string eg. 3/17/2021 at 1:29 PM
 */
const Date = (
  value,
  format = "M/D/YYYY [at] h:mm A",
  local = false,
  noSuffix = false
) => {
  if (!value) return null

  let date = dayjs(value)

  if (!date.isValid()) return null

  if (format === "relative") {
    if (date.isBefore()) {
      return date.fromNow(noSuffix)
    }
    return dayjs().fromNow(noSuffix)
  }

  if (format === "calendar") return date.calendar()

  if (local) return date.tz().format(format)

  return date.format(format)
}

/**
 * Formats a datetime field to calendar relative date.
 * Converts date in calendar format like Yesterday, Today, Last Saturday for a week
 * else convert it into relative date like a month ago, a year ago
 *
 * @param {string} value input string
 * @returns {string} date
 */
const DateRelative = (value) => {
  let dateTime = dayjs(value)
  let otherDates = dateTime.fromNow()
  let week = dateTime.calendar()
  let calback = () => otherDates
  let weekcal = () => week.split(" at ")[0]
  return dateTime.calendar(null, {
    sameDay: "Today",
    nextDay: weekcal,
    nextWeek: calback,
    lastDay: weekcal,
    lastWeek: weekcal,
    sameElse: calback,
  })
}

/**
 * Formats any empty data field with a placeholder.
 *
 * @param {*} value Empty string eg. ""
 * @param {string} placeholder Placeholder eg. "N/A"
 * @returns {string} Formatted empty data field eg. "N/A"
 */
const Empty = (value, placeholder = "—") => {
  if (String(value).trim() === "" || value === null || value === undefined) {
    return placeholder
  }
  return value
}

const Numeric = (
  value,
  round = false,
  abbreviate = false,
  approx = false,
  percentage = false,
  append = ""
) => {
  if (typeof value !== "number") return value
  let abrv = ""

  if (percentage) {
    value = value * 100
    append = "%"
  }

  if (abbreviate) {
    if (value >= 1000000) {
      value = value / 1000000
      abrv = "M"
    } else if (value >= 1000) {
      value = value / 1000
      abrv = "K"
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
    : value
        .toLocaleString("en-US", {
          minimumFractionDigits: 0,
          maximumFractionDigits: round && Number(value) ? 0 : 2,
        })
        .replace(/\B(?=(\d{3})+(?!\d))/g, ",") +
        abrv +
        append
}

/**
 * Formats a string with title case.
 *
 * @param {*} value The string eg. "active Customers"
 * @returns {string} Title cased string eg. "Active Customers"
 */
const TitleCase = (value) => {
  return value.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  })
}

/**
 * Formats any string(fullname) to shortname.
 *
 * @param {*} value The string eg. "John petro"
 * @returns {string} shortname string eg. "JP"
 */
const shortName = (value) => {
  return value
    .split(" ")
    .map((n) => n[0])
    .join("")
}

const Currency = (value) => {
  if (isNaN(value)) return "-"
  return Number(value).toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })
}

/**
 * Formats as a percentage.
 *
 * @param {*} value The input eg. "0.893251"
 * @param {boolean} round whether to round the value
 * @returns {string} output value eg. "89%" or "89.32%"
 */
const Percentage = (value, round = true) => {
  return Numeric(value, round, false, false, true)
}

/**
 *
 * @param {*} value This input eg. ""
 * @returns {string} output value eg. "—" if no value,
 *                               if value has schedule for both start and end dates, then "Aug 12 - Sep 10"
 *                               if value has start date but no end date then "Aug 12 - No End"
 *                               if the value is 'Manual' then 'Manual'
 */
const DeliverySchedule = (value) => {
  if (!value) return "Manual"
  if (value instanceof Object) {
    return (
      `${Date(value.start_date, "MMM DD")}` +
      " - " +
      (value.end_date ? Date(value.end_date, "MMM DD") : "No End")
    )
  } else {
    return value
  }
}

export default {
  Date,
  DateRelative,
  Empty,
  Numeric,
  TitleCase,
  shortName,
  Currency,
  Percentage,
  DeliverySchedule,
}
