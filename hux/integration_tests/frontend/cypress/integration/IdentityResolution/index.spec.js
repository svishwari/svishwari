import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Data management > Identity resolution", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to view the overview", () => {
    cy.location("pathname").should("eq", route.overview)

    //click on identity resolution on side nav bar
    cy.get(selector.idr.identityResolution).click()
    cy.location("pathname").should("eq", route.identityResolution)
  })

  it("should be able to view the matching trends", () => {
    //validate overview exist by getting total no. of them
    cy.get(selector.idr.overview).its("length").as("overviewListCount")
    cy.get("@overviewListCount").then((overviewListCount) => {
      cy.get(selector.idr.overview).its("length").should("eq", 7)
    })
  })

  it("should be able to view the data feeds", () => {
    //validate data feed
    cy.get(selector.idr.datafeed).its("length").as("datafeedListCount")
    cy.get("@datafeedListCount").then((datafeedListCount) => {
      cy.get(selector.idr.datafeed).its("length").should("gt", 0)
    })
  })
})
