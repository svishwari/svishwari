// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

import route from "./routes.js"
import selector from "./selectors.js"

Cypress.Commands.add("signin", ({ email, password }) => {
  // opens the app
  cy.visit(route.index)

  // clicks the signin button
  cy.get(selector.app.signin).click()

  // we should now be on the login page
  cy.location("pathname").should("eq", route.login)

  // fill in the form
  cy.get(selector.login.email).type(email, { log: false })

  cy.get(selector.login.password).type(password, {
    log: false,
  })

  cy.get(selector.login.remember).click()

  // submit the form
  cy.get(selector.login.submit).click()

  // TODO: add MFA related authentication if needed

  // we should no longer be on the login page
  cy.location("pathname", { timeout: 10000 })
    .should("not.eq", route.login)
    .then(() => {
      // okta does its authentication...
      // once its done, we should be redirected back to the app
      cy.location("pathname").should("eq", route.oktaSignInRedirectURI)
    })
})

Cypress.Commands.add("reLogin", () => {
  const email = Cypress.env("USER_EMAIL")
  const password = Cypress.env("USER_PASSWORD")

  cy.location("pathname").should("eq", route.login)

  cy.get(selector.login.email).type(email, { log: false })

  cy.get(selector.login.password).type(password, {
    log: false,
  })

  cy.get(selector.login.remember).click()

  // submit the form
  cy.get(selector.login.submit).click()
})
