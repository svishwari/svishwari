/**
 * Globally registered Vue filters
 */
import dayjs from "dayjs"
import calendar from "dayjs/plugin/calendar"
import relativeTime from "dayjs/plugin/relativeTime"

dayjs.extend(calendar)
dayjs.extend(relativeTime)
/**
 * Formats a datetime field to human friendly date.
 *
 * @param {*} value Datetime eg. 2021-03-17T13:29:49.351Z
 * @param {*} format Format eg. "MM/D/YYYY [at] hh:ss A"
 * @return {string} Formatted date time string eg. 3/17/2021 at 1:29 PM
 */
const Date = (value, format = "M/D/YYYY [at] h:mm A", noSuffix = false) => {
  if (!value) return ""

  let date = dayjs(value)

  if (format === "relative") {
    if (date.isBefore()) {
      return date.fromNow(noSuffix)
    }
    return dayjs().fromNow(noSuffix)
  }

  if (format === "calendar") return date.calendar()

  return date.format(format)
}
/**
 * Formats a datetime field to calendar relative date.
 * Converts date in calendar fromat like Yesterday, Today, Last Saturday for a week
 * else convert it into relative date like a month ago, a year ago
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
 * @param {*} placeholder Placeholder eg. "N/A"
 * @returns Formatted empty data field eg. "N/A"
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
    : value.toLocaleString("en-US", {
        minimumFractionDigits: 0,
        maximumFractionDigits: round && Number(value) ? 0 : 2,
      }) +
        abrv +
        append
}

/**
 * Formats a string with title case.
 *
 * @param {*} value The string eg. "active Customers"
 * @returns Title cased string eg. "Active Customers"
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
 * @returns shortname string eg. "JP"
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
 * @returns output value eg. "89%" or "89.32%"
 */
const Percentage = (value, round = true) => {
  return Numeric(value, round, false, false, true)
}
/**
 *
 * @param {*} value This input eg. ""
 * @returns output value eg. "—" if no value,
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
