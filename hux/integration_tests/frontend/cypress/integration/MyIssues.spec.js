import route from "../support/routes.js"
import selector from "../support/selectors.js"

describe("My issues", () => {
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
    cy.get(selector.myIssues.wrapper).then((elem) => {
      if (elem.find(selector.myIssues.table).length > 0) {
        cy.get(selector.myIssues.table).should("exist")
        cy.get(selector.myIssues.key).its("length").should("gte", 0)
        cy.get(selector.myIssues.status).its("length").should("gte", 0)
        cy.get(selector.myIssues.summary).its("length").should("gte", 0)
        cy.get(selector.myIssues.time).its("length").should("gte", 0)
      } else if (elem.find(".background-empty").length > 0) {
        cy.wrap(".background-empty").should("exist")
      } else {
        cy.wrap(".error-screen").should("exist")
      }
    })
    cy.get(selector.myIssues.return).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.location("pathname").should("eq", route.home)
  })
})
