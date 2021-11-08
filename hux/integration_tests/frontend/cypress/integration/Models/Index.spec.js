import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("View models", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.models)
  })

  it("should be able to view a list of models", () => {
    cy.location("pathname").should("eq", route.models)

    cy.get(selector.models.item).its("length").should("gt", 0)

    cy.get(selector.models.item).should(($models) => {
      expect($models.eq(0).find(selector.card.title)).to.contain(
        "Pendleton Unsubscribe Model",
      )
      expect($models.eq(0).find(selector.card.description)).to.contain(
        "Predicts the propensity of a customer to unsubscribe",
      )

      expect($models.eq(1).find(selector.card.title)).to.contain(
        "Propensity to Purchase",
      )
      expect($models.eq(1).find(selector.card.description)).to.contain(
        "Propensity of a customer making a purchase after receiving an email",
      )

      expect($models.eq(2).find(selector.card.title)).to.contain(
        "Propensity to Unsubscribe",
      )
      expect($models.eq(2).find(selector.card.description)).to.contain(
        "Predicts the propensity of a customer to unsubscribe from an email list",
      )
    })
  })
})
