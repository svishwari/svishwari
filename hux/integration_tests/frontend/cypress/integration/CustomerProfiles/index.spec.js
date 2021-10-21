import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Data management > Customer Profiles", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should have an Overview, Total customers, Geographic and Demographic charts", () => {
    cy.location("pathname").should("eq", route.overview)

    // click on customer profiles on side nav bar
    cy.get(selector.customerProfile.customers).click()
    cy.location("pathname").should("eq", route.customerProfiles)

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    // should be able to view overview of customer profiles"
    cy.get(selector.customerProfile.overview)
      .its("length")
      .as("overviewListCount")
    cy.get("@overviewListCount").then(() => {
      cy.get(selector.customerProfile.overview).its("length").should("eq", 8)
    })

    // should be able to view customer overview of customer profiles"
    cy.get(selector.customerProfile.customeroverview)
      .its("length")
      .as("customeroverviewListCount")

    cy.get("@customeroverviewListCount").then(() => {
      cy.get(selector.customerProfile.customeroverview)
        .its("length")
        .should("eq", 8)
    })

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)

    // should be able to check if valid response for total customers has received"
    cy.get(selector.customerProfile.chart).its("length").should("gt", 0)

    // should be able to hover over state"
    cy.get(".state")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // map state list should have a list of states"
    cy.get(selector.customerProfile.mapStateList)
      .its("length")
      .should("gte", 51)

    // should be able to view top location & income chart"
    // validate top location & income chart
    cy.get(selector.customerProfile.incomeChart).its("length").should("gt", 0)

    // should be able to hover over bar of top location & income chart"
    // mouse hover on income chart
    cy.get(".bar")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // should be able to view Gender / monthly spending chart"
    cy.get(selector.customerProfile.genderSpendChart)
      .its("length")
      .should("gt", 0)

    // should be able to view Gender chart"
    cy.get(selector.customerProfile.genderChart).its("length").should("gt", 0)

    // should be able to hover over arc of gender chart"
    cy.get(".arc")
      .first()
      .trigger("mouseover", { force: true, eventConstructor: "MouseEvent" })
  })
})
