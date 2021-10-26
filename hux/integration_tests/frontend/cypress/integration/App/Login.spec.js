import route from "../../support/routes.js"

describe("Login", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to login and view the overview", () => {
    cy.location("pathname").should("eq", route.overview)
  })
})
