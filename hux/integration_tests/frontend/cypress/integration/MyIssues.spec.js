import route from "../support/routes.js"
import selector from "../support/selectors.js"

describe("Navigation", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.home)
  })

  it("should be able to explore my issues", () => {
    cy.visit(route.myIssues)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.location("pathname").should("eq", route.myIssues)
    cy.get(selector.myIssues.header).should("exist")
    cy.get(selector.myIssues.table).should("exist")
    cy.get(selector.myIssues.key).its("length").should("gte", 0)
    cy.get(selector.myIssues.status).its("length").should("gte", 0)
    cy.get(selector.myIssues.summary).its("length").should("gte", 0)
    cy.get(selector.myIssues.time).its("length").should("gte", 0)
    cy.get(selector.myIssues.return).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.location("pathname").should("eq", route.home)
  })
})
