import route from "../../support/routes.js"
import selector from "../../support/selectors.js"
import { randomText } from "../../support/utils.js"

describe("Orchestration > Audience > Create Audience", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to configure a new audience", () => {
    // should be able to navigate to audience and click on add audience button
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    //click on audience on side nav bar and route in audience screen
    cy.get(selector.audiences).click()
    cy.location("pathname").should("eq", route.audiences)
    //click on add audience button
    cy.get(selector.audience.addAudiences).click()

    // should fill new audience name and description
    // add new audience name
    cy.get(selector.audience.audienceName).eq(0).type(randomText())

    // should add audience to the audience
    // Click on add audience icon
    cy.get(selector.audience.addEngagement).click()
    // Select the first audience from the existing ones
    cy.get(selector.audience.selectEngagement).eq(0).click()
    // Click on outside the close the add audience Drawer
    cy.get(selector.engagement.exitDrawer).click()

    // should add destination to the audience
    // Click on add audience icon
    cy.get(selector.audience.addDestination).click()
    // Select the first destination from the existing ones
    cy.get(selector.engagement.selectDestination).eq(0).click()
    cy.get(selector.engagement.exitDrawer).click()
    cy.get(selector.audience.createAudience).click()
  })

  it("should add destination data extensions and verify the configuration", () => {
    // TODO: add a check that it requires data extension name before proceeding
    cy.get(selector.audience.addDestination).click()
    cy.get("body").then(($body) => {
      if ($body.find(selector.audience.salesForceAddButton).length > 0) {
        cy.get(selector.audience.salesForceAddButton).click()
        // Add new data extension name
        cy.get(selector.engagement.dataExtensionName).eq(1).type(randomText())
        // Close the data extension drawer
        cy.get(selector.engagement.exitDataExtensionDrawer).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)
        // Close the add destination drawer
        cy.get(selector.engagement.exitDrawer).click()
      }
    })
  })
})
