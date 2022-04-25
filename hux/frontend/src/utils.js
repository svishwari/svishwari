/**
 * Utilities
 */

import dayjs from "dayjs"
import store from "@/store/index.js"
import { capitalize } from "lodash"

/**
 * Forms the title for the page.
 *
 * @param {string} title - The title of the page
 * @returns {string} The page title
 */
export function pageTitle(title) {
  return `${title} · Hux`
}

/**
 * Handles an error.
 *
 * @param {string} error
 * eslint-disable-next-line jsdoc/require-returns-check
 */
export function handleError(error) {
  // TODO: do more with the error than just logging it to the console
  let errorMessage =
    error.response.data.message ||
    error.response.data.exception_message ||
    error.message
  store.dispatch("alerts/setAlert", {
    message: errorMessage,
    code: error.response.status,
    type: "error",
  })
}

/**
 * Handles an Success Message.
 *
 * @param {string} message
 * eslint-disable-next-line jsdoc/require-returns-check
 * @param {number} status
 * eslint-disable-next-line jsdoc/require-returns-check
 */
export function handleSuccess(message, status) {
  store.dispatch("alerts/setAlert", {
    message: message,
    code: status,
    type: "success",
  })
}

/**
 * Handles an info Message.
 *
 * @param {string} message
 * eslint-disable-next-line jsdoc/require-returns-check
 * @param {number} status
 * eslint-disable-next-line jsdoc/require-returns-check
 */
export function handleInfo(message, status) {
  store.dispatch("alerts/setAlert", {
    message: message,
    code: status,
    type: "info",
  })
}

/**
 * Get color HEX code
 *
 * @param {*} str string to generate color from
 * @param {*} s ?
 * @param {*} l ?
 * @returns {string} hex code
 */
export function generateColor(str, s, l) {
  /**
   * @param {*} h ?
   * @param {*} s ?
   * @param {*} l ?
   * @returns {string} hex
   */
  function hslToHex(h, s, l) {
    l /= 100
    const a = (s * Math.min(l, 1 - l)) / 100
    const f = (n) => {
      const k = (n + h / 30) % 12
      const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1)
      return Math.round(255 * color)
        .toString(16)
        .padStart(2, "0") // convert to Hex and prefix "0" if needed
    }
    return `#${f(0)}${f(8)}${f(4)}`
  }
  var hash = 0
  for (var i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }

  var h = hash % 360
  return hslToHex(h, s, l)
}

/**
 * getApproxSize
 *
 * @param {number} value number
 * @returns {string} approximate size
 */
export function getApproxSize(value) {
  // Nine Zeroes for Billions
  return Math.abs(Number(value)) >= 1.0e9
    ? (Math.abs(Number(value)) / 1.0e9).toFixed(2) + "B"
    : // Six Zeroes for Millions
    Math.abs(Number(value)) >= 1.0e6
    ? (Math.abs(Number(value)) / 1.0e6).toFixed(2) + "M"
    : // Three Zeroes for Thousands
    Math.abs(Number(value)) >= 1.0e3
    ? (Math.abs(Number(value)) / 1.0e3).toFixed(2) + "K"
    : Math.abs(Number(value))
}

/**
 * Extracts audiences that have destinations passed in the params
 *
 * @param {Array} audiences List of audiences
 * @param {Array} destinations List of destination to match
 * @returns {string} List of filtered audiences
 */
export function filterAudiencesByDestinations(audiences, destinations = []) {
  let filteredAudiences = audiences.filter((audience) => {
    let isRequiredDestinationPresent = false
    if (audience.destinations) {
      isRequiredDestinationPresent =
        audience.destinations.findIndex((destination) =>
          destinations.includes(destination.type)
        ) !== -1
          ? true
          : false
    }
    return isRequiredDestinationPresent
  })

  return filteredAudiences
}

/**
 * Uses to initialize or reset while using hux-schedule-picker component
 *
 * @param {object} schedule schedule
 * @returns {object} delivery schedule
 */
export function deliverySchedule(schedule = {}) {
  let defaultSchedule = {
    periodicity: "Daily",
    every: 1,
    hour: 12,
    minute: 15,
    period: "AM",
    monthlyPeriod: "Day",
    monthlyDay: ["Day"],
    monthlyDayDate: [1],
    day_of_week: ["SUN"],
  }
  if (schedule) {
    for (let prop in schedule) {
      defaultSchedule[prop] =
        prop in schedule ? schedule[prop] : defaultSchedule[prop]
    }
  }
  return defaultSchedule
}

/**
 * Uses to create abbr for day names with uppercase
 *
 * @param {string} dayname full name
 * @returns {string} day name abbr i.e. SUN
 */
export function dayAbbreviation(dayname) {
  let abbr = ""
  if (dayname) {
    abbr = dayname.substring(0, 3).toUpperCase()
  }
  return abbr
}

/**
 * Uses to create full name from abbr
 *
 * @param {string} dayname abr name
 * @returns {string} day full name i.e. Sunday
 */
export function abbrDayToFullName(dayname) {
  switch (dayname.toLowerCase()) {
    case "mon":
      return "Monday"
    case "tue":
      return "Tuesday"
    case "wed":
      return "Wednesday"
    case "thu":
      return "Thursday"
    case "fri":
      return "Friday"
    case "sat":
      return "Saturday"
    case "sun":
      return "Sunday"
    default:
      return ""
  }
}

/**
 * Get a list of months names.
 *
 * @param {object} config configuration for list of months
 * @param {string} config.startMonth the first month in list. Default: "January"
 * @param {string} config.endMonth the last month in list. Default: "December"
 * @param {boolean} config.inclusive whether to include the selected months or not. Default: true
 * @returns {string[]} list of months in the range provided
 */
export function listOfMonths(config = {}) {
  const { startMonth, endMonth } = config

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ]

  if (startMonth || endMonth) {
    const startIndex = months.indexOf(startMonth || "January")
    const endIndex = months.indexOf(endMonth || "December") + 1
    const selectedMonths = months.slice(startIndex, endIndex)
    return selectedMonths
  }

  return months
}

/**
 * Get a list of years.
 *
 * @param {object} config configuration for list of years
 * @param {string} config.startYear the first year to start from. Default: "2015"
 * @param {string} config.endYear the last year to end on. Default: "2021"
 * @returns {string[]} list of years
 */
export function listOfYears(
  config = {
    startYear: dayjs().subtract(4, "year").format("YYYY"),
    endYear: dayjs().format("YYYY"),
  }
) {
  let min = Number(config.startYear)
  let max = Number(config.endYear)
  let years = []
  for (let i = min; i <= max; i++) {
    years.push(min.toString())
    min++
  }
  return years
}

/**
 * Gets the last date of the month.
 *
 * @param {string} date a date which to get the last date of the month
 * @returns {string} the date at the end of month
 */
export function endOfMonth(date) {
  return dayjs(date).endOf("month").format("YYYY-MM-DD")
}

/**
 * Download file from the blob API response.
 *
 * @param {*} response
 * eslint-disable-next-line jsdoc/require-returns-check
 */
export function saveFile(response) {
  const fileName = response.headers["content-disposition"].match(
    /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
  )[1]
  const link = document.createElement("a")
  link.href = window.URL.createObjectURL(
    new Blob([response.data], {
      type: response.headers["content-type"],
    })
  )
  link.download = fileName
  link.click()
  URL.revokeObjectURL(link.href)
}

/**
 * Return true if column has multiple values.
 *
 * @param {object[]} data - response data as an array of objects
 * @param {string} field - field name
 * @returns {boolean} true if column has multiple values else false
 */
export function arrayHasFieldWithMultipleValues(data, field) {
  let colData = data.map((x) => x[field])
  return Boolean(new Set(colData).size > 1)
}

/**
 * Returns the list of objects in array as a group by Key
 *
 * @param {object[]} array - array of objects
 * @param {string} key - the group by key
 * @returns {object} - Returns the object with grouped by key and unique values
 */
export function groupBy(array, key) {
  array = array.map((obj) => ({ ...obj, category: obj["category"] || "Other" }))
  return array.reduce((hash, obj) => {
    if (obj[key] === undefined) return hash
    return Object.assign(hash, {
      [obj[key]]: (hash[obj[key]] || []).concat(obj),
    })
  }, {})
}

/**
 * Returns the list of objects in sorted
 *
 * @param {object} data - object with each key having array
 * @param {string} key - the group by key
 */
export function sortByName(data, key) {
  Object.values(data).forEach((val) => {
    val.sort(function (a, b) {
      var textA = a[key].toUpperCase()
      var textB = b[key].toUpperCase()
      return textA < textB ? -1 : textA > textB ? 1 : 0
    })
  })
}

/**
 * Returns the string in Sentence Case
 *
 * @param {string} text - string to be formatted
 * @returns {string} formatted string
 */
export function formatText(text) {
  return capitalize(text.replaceAll("_", " "))
}

/**
 * Returns the string with space replaced with Underscore & Lower Case
 *
 * @param {string} text - string to be formatted
 * @returns {string} formatted string
 */
export function formatRequestText(text) {
  return text.replaceAll(" ", "_").toLowerCase()
}

/**
 * Returns grouped month year from GMT time stamp
 *
 * @param {string} date - date to be formatted
 * @returns {string} formatted date
 */
export function formatDate(date) {
  return dayjs(date).format("MMM DD")
}

/**
 * Returns minimum date for enddate time picker converted to ISO format string
 *
 * @returns {string} formatted HTML
 */
export function endMinDateGenerator() {
  return new Date(
    new Date().getTime() - new Date().getTimezoneOffset() * 60000
  ).toISOString()
}

/**
 * Returns local time zone
 *
 * @param {string} date - date to be formatted
 * @returns {string} formatted date
 */
export function formatDateToLocal(date) {
  let res = dayjs(date).local().format("DD/MM/YYYY hh:mm a zzz")
  let timezone = res.split("m ")[1]
  timezone = timezone.split(" ")
  let tz = ""
  timezone.forEach((x) => {
    tz += x[0]
  })
  return res.split("m ")[0] + "m " + tz
}
/**
 * Returns innerHTML
 *
 * @param {string} text - string to be formatted to HTML
 * @returns {string} formatted HTML
 */
export function formatInnerHTML(text) {
  return { innerHTML: text }
}

/**
 * Returns number converted to string with commas
 *
 * @param {string} num - number to be formatted to string
 * @returns {string} formatted number
 */
export function numberWithCommas(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

/**
 * Returns initial and batch count for request
 *
 * @param {object} request - request for calculating batch size and count
 * @returns {Array} array of strings
 */
export function getBatchCounts(request) {
  let currentBatch =
    request.queryParams.batch_number || request.queryParams.batchNumber
  let batchSize =
    request.queryParams.batch_size || request.queryParams.batchSize
  let initialCount = currentBatch == 1 ? 0 : (currentBatch - 1) * batchSize
  let lastCount = currentBatch == 1 ? batchSize : currentBatch * batchSize
  return [initialCount, lastCount]
}

/**
 * Returns array of aggregated filters for age type filter only
 *
 * @param {object} filters - filters to be aggregated
 * @returns {Array} array of strings
 */
export function aggregateAgeFilters(filters) {
  if (!filters || filters.length == 0) {
    return []
  }
  let numericFilters = []
  let stringFilters = []
  let [aggregatedFilterStart, aggregatedFilterEnd] = filters[0]
    .split("-")
    .map((val) => parseInt(val))
  filters.forEach((filter) => {
    let [currentFilterStart, currentFilterEnd] = filter
      .split("-")
      .map((val) => parseInt(val))
    if (!currentFilterStart) {
      stringFilters.push(filter)
    } else if (
      currentFilterStart == aggregatedFilterStart ||
      currentFilterStart == aggregatedFilterEnd + 1
    ) {
      aggregatedFilterEnd = currentFilterEnd
    } else {
      numericFilters.push(
        `${aggregatedFilterStart}-${aggregatedFilterEnd} years`
      )
      aggregatedFilterStart = currentFilterStart
      aggregatedFilterEnd = currentFilterEnd
    }
  })
  if (aggregatedFilterStart) {
    numericFilters.push(`${aggregatedFilterStart}-${aggregatedFilterEnd} years`)
  }
  return [...numericFilters, ...stringFilters]
}
