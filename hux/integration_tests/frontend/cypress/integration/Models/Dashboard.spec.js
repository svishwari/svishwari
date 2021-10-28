import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Decisioning > models", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.models)
  })

  it("should be able to view a model's dashboard", () => {
    cy.location("pathname").should("eq", route.models)

    cy.get(selector.models.item).its("length").should("gt", 0)

    cy.get(selector.models.item).first().click()

    // should be able to view model overview
    cy.get(selector.models.performancemetric)
      .its("length")
      .as("overviewListCount")

    cy.get("@overviewListCount").then(() => {
      cy.get(selector.models.performancemetric).its("length").should("eq", 5)
    })

    // should be able to view and validate Drift and Feature chart
    cy.get(selector.models.driftchart).its("length").should("be.gt", 0)
    cy.get(selector.models.featurechart).its("length").should("be.gt", 0)

    // scroll down
    cy.scrollTo("bottom", { duration: 1000 })

    // should be able to hover over Feature chart"
    cy.get(".bar")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // validate feature and lift table
    cy.get(selector.models.lifttable).its("length").should("be.gt", 0)
    cy.get(selector.models.featuretable).its("length").should("be.gt", 0)

    // should be able to view version history list
    cy.get(selector.models.modelDashboardOptions).find("svg").click()
    cy.get(selector.models.versionhistorybutton).click()

    //validate the history list
    cy.get(selector.models.versionhistory).its("length").should("gt", 0)
  })
})
