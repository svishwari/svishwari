/**
 * Utilities
 */

/**
 * Forms the title for the page.
 *
 * @param {string} title - The title of the page
 * @return {string} The page title
 */
export function pageTitle(title) {
  return `${title} · Hux`
}

/**
 * Handles an error.
 *
 * @param {string} error
 */
export function handleError(error) {
  // TODO: do more with the error than just logging it to the console
  console.error(error)
}
/**
 * get color HEX code
 *
 * @param {string} error
 */
export function generateColor(str, s, l) {
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
 * @param {Array} destinations - List of destination to match
 * @return {string} List of filtered audiences
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
 * @returns {Object} 
 */
export function deliverySchedule() {
  return {
    "periodicity": "Daily",
    "every": 1,
    "hour": 12,
    "minute": 15,
    "period": "AM",
    "monthlyPeriod": "Day",
    "monthlyDay": "Day",
    "monthlyDayDate": 1,
    "days": ["Sunday"]
  }
}