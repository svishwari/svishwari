import route from "../support/routes.js"

describe("Login", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.home)
  })

  it("should be able to login and view the home", () => {
    cy.location("pathname").should("eq", route.home)
  })
})
