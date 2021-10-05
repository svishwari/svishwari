import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Data management > Identity resolution", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should have an Overview, Matching trends and Data feeds table with Last run drawer", () => {
    cy.location("pathname").should("eq", route.overview)

    // click on identity resolution on side nav bar
    cy.get(selector.idr.identityResolution).click()
    cy.location("pathname").should("eq", route.identityResolution)

    // validate overview exist by getting total no. of them
    cy.get(selector.idr.overview).its("length").as("overviewListCount")
    cy.get("@overviewListCount").then((overviewListCount) => {
      cy.get(selector.idr.overview).its("length").should("eq", 7)
      cy.get(selector.idr.overview)
        .its("length")
        .should("eq", overviewListCount)
    })

    // validate data feed
    cy.get(selector.idr.datafeed).its("length").as("datafeedListCount")
    cy.get("@datafeedListCount").then((datafeedListCount) => {
      cy.get(selector.idr.datafeed).its("length").should("gt", 0)
      cy.get(selector.idr.datafeed)
        .its("length")
        .should("eq", datafeedListCount)
    })

    // open last run drawer
    cy.get(selector.idr.lastrun).first().click()

    // toggle pinning panel open/closed
    cy.get(selector.idr.pinning).click()
    cy.get(selector.idr.pinning).click()

    // toggle stitched panel open/closed
    cy.get(selector.idr.stitched).click()
    cy.get(selector.idr.stitched).click()
  })
})
