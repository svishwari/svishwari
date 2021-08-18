import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("View models", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to view a list of models", () => {
    cy.get(selector.nav.models).click()

    cy.location("pathname").should("eq", route.models)

    cy.get(selector.models.item).should(($models) => {
      expect($models).to.have.length(2)

      // propensity to unsubscribe model
      expect($models.eq(0).find(selector.card.title)).to.contain(
        "Propensity to Unsubscribe",
      )
      expect($models.eq(0).find(selector.card.description)).to.contain(
        "Propensity of a customer unsubscribing to emails.",
      )

      // LTV model
      expect($models.eq(1).find(selector.card.title)).to.contain("LTV")
      expect($models.eq(1).find(selector.card.description)).to.contain(
        "Propensity of a customer unsubscribing to emails.",
      )
    })
  })
})
