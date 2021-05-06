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
