import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("View models", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.models)
  })

  it("should be able to view a list of models", () => {
    cy.location("pathname").should("eq", route.models)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.models.item).its("length").should("gt", 0)

    cy.get(selector.models.item).each(($models) => {
      cy.wrap($models)
        .get(selector.models.activeStatus)
        .children()
        .eq(0)
        .should("satisfy", ($el) => {
          const classList = Array.from($el[0].classList)
          return (
            classList.includes("success--text") ||
            classList.includes("primary--text")
          ) // passes
        })
    })
  })
})
