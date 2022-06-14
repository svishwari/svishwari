import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Data management > Identity resolution", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.identityResolution)
  })

  it("should have an Overview, Matching trends and Data feeds table with Last run drawer", () => {
    cy.location("pathname").should("eq", route.identityResolution)

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)

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
    cy.get(selector.idr.stitched).click()

    // toggle stitched panel open/closed
    cy.get(selector.idr.stitched).click()
    cy.get(selector.idr.stitched).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    //click ouside to close the drawer
    cy.get(selector.idr.exitDrawer).click()
    if (cy.get(selector.idr.datafeed).its("length").should("gt", 0)) {
      cy.get(selector.idr.idrfilterToggle).click()
      cy.get(selector.idr.selectDate).click()
      cy.get('.hux-select')
      cy.get('[role="listbox"]').children().eq(0).click()
      // eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(500)
      cy.get(selector.idr.applyIdrFilter).click()
      // eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(3000)
      cy.get(selector.idr.closeIdrFilter).click()
      cy.get(selector.idr.idrfilterToggle).click()
      cy.get(selector.idr.clearIdrFilter).click()
      // eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(2000)
      cy.get(selector.idr.closeIdrFilter).click()
    }

  })
})
