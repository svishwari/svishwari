import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Data management > Customer Profiles", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to view the overview", () => {
    cy.location("pathname").should("eq", route.overview)

    //click on customer profiles on side nav bar
    cy.get(selector.customerProfile.customers).click()
    cy.location("pathname").should("eq", route.customerProfiles)
  })

  it("should be able to view overview of customer profiles", () => {
    //validate overview exist by getting total no. of them
    cy.get(selector.customerProfile.overview)
      .its("length")
      .as("overviewListCount")
    cy.get("@overviewListCount").then(() => {
      cy.get(selector.customerProfile.overview).its("length").should("eq", 8)
    })
  })

  it("should be able to view customer overview of customer profiles", () => {
    //validate customer overview exist by getting total no. of them
    cy.get(selector.customerProfile.customeroverview)
      .its("length")
      .as("customeroverviewListCount")
    cy.get("@customeroverviewListCount").then(() => {
      cy.get(selector.customerProfile.customeroverview)
        .its("length")
        .should("eq", 8)
    })
  })

  it("should be able to check if valid response for total customers has received", () => {
    //validate Total Customer response
    cy.get(selector.customerProfile.chart).its("length").should("gt", 0)
  })

  it("should be able to hover over state", () => {
    // mouse hover on state
    cy.get(".state")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })
  })

  it("map state list should have 51 state", () => {
    // validate no of state in list
    cy.get(selector.customerProfile.mapStateList).its("length").should("eq", 51)
  })

  it("should be able to view top location & income chart", () => {
    // validate top location & income chart
    cy.get(selector.customerProfile.incomeChart).its("length").should("gt", 0)
  })

  it("should be able to hover over bar of top location & income chart", () => {
    // mouse hover on income chart
    cy.get(".bar")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })
  })

  it("should be able to view Gender / monthly spending chart", () => {
    //validate Gender / monthly spending chart
    cy.get(selector.customerProfile.genderSpendChart)
      .its("length")
      .should("gt", 0)
  })

  it("should be able to view Gender chart", () => {
    //validate Gender chart
    cy.get(selector.customerProfile.genderChart).its("length").should("gt", 0)
  })

  it("should be able to hover over arc of gender chart", () => {
    // mouse hover on income chart
    cy.get(".arc")
      .first()
      .trigger("mouseover", { force: true, eventConstructor: "MouseEvent" })
  })
})
