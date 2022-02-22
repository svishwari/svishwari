import route from "../support/routes.js"
import selector from "../support/selectors.js"

describe("Applications", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.home)
  })

  it("should be able to explore the features in adding an application", () => {
    cy.visit(route.addApplication)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.location("pathname").should("eq", route.addApplication)
    cy.get(selector.application.addDrawer).click()
    cy.get(selector.application.applications).its("length").should("gt", 0)
    cy.get(selector.application.cancel).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.location("pathname").should("eq", route.home)
  })
})
