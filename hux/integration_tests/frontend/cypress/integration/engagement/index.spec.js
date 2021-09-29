import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Orchestration > Engagement > Create Engagement", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to navigate to engagement and click on add engagement button", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    //click on engagement on side nav bar and route in engagement screen 
    cy.get(selector.engagements).click()
    cy.location("pathname").should("eq", route.engagements)
    //click on add engagement button 
    cy.get(selector.engagement.addEngagements).click()
  })

  it("should fill new engagement name and description", () => {
    // add new engagement name
    cy.get(selector.engagement.enagagementName).eq(0).type("Test Engagement")
    // add new engagement description
    cy.get(selector.engagement.enagagementDescription).eq(0).type("Engagement for E2E testing")
  })

  it("should add audience to the enagement", () => {
    // Click on add audience icon
    cy.get(selector.engagement.addAudience).click()
    // Select the first audience from the existing ones
    cy.get(selector.engagement.selectAudience).eq(0).click()
    // Click on outside the close the add audience Drawer
    cy.get(selector.engagement.exitDrawer).click()
  })

  it("should add destination to the enagement", () => {
    // Click on add audience icon
    cy.get(selector.engagement.addDestination).click()
    // Select the first audience from the existing ones
    cy.get(selector.engagement.selectDestination).eq(0).click()
  })

  it("should add destination data extensions and verify the configuration", () => {
    // Add new data extension name
    cy.get(selector.engagement.dataExtensionName).eq(0).type("Testing")
    // Close the data extension drawer
    cy.get(selector.engagement.exitDataExtensionDrawer).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    // Close the add destination drawer (as per updated flow)
    cy.get(selector.engagement.exitDrawer).click()
  })
})
