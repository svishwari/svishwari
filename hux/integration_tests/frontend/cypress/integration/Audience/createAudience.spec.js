import route from "../../support/routes.js"
import selector from "../../support/selectors.js"
import { randomName } from "../../support/utils.js"

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
    cy.get(selector.audience.audienceName)
      .eq(0)
      .type(`E2E test audience (${randomName()})`)

    // should add audience to the audience
    // Click on add audience icon
    cy.get(selector.audience.addEngagement).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    cy.get("body").then(($body) => {
      if ($body.find(selector.audience.selectEngagement).length > 0) {
        // Select the first audience from the existing ones
        cy.get(selector.audience.selectEngagement).eq(0).click()
      } else if ($body.find(selector.audience.newEngagementFirst).length > 0) {
        cy.get(selector.audience.newEngagementFirst).click()
        cy.get(selector.audience.newEngagementFirstName)
          .eq(0)
          .type(`E2E test engagement (${randomName()})`)
        cy.get(selector.audience.createNewEngagement).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)
      }
    })

    // Click on outside the close the add audience Drawer
    cy.get(selector.engagement.exitDrawer).click()

    // should add destination to the audience
    // Click on add audience icon
    cy.get(selector.audience.addDestination).click()
    // Select the first destination from the existing ones
    cy.get(selector.engagement.selectDestination).eq(0).click()
    cy.get(selector.engagement.exitDrawer).click()

    // should add destination data extensions and verify the configuration
    cy.get(selector.audience.addDestination).click()
    cy.get("body").then(($body) => {
      if ($body.find(selector.audience.salesForceAddButton).length > 0) {
        cy.get(selector.audience.salesForceAddButton).click()
        // Add new data extension name
        cy.get(selector.engagement.dataExtensionName)
          .eq(1)
          .type(`New Data Extension`)
        // Close the data extension drawer
        cy.get(selector.engagement.exitDataExtensionDrawer).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)
        // Close the add destination drawer
        cy.get(selector.engagement.exitDrawer).click()
      }
    })

    cy.get(selector.audience.createAudience).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)
    cy.location("pathname").should("contain", "insight")
    cy.get(selector.audiences).eq(0).click()
    // delete created audience
    cy.location("pathname").should("eq", route.audiences)
    cy.get(selector.audience.audiencelist).its("length").should("be.gt", 0)
    cy.get(selector.audience.audiencenameclick)
      .eq(0)
      .find("button")
      .eq(1)
      .click({ force: true })
    cy.get(".v-menu__content").should("exist")

    cy.contains("Delete audience").eq(0).click()

    cy.get(selector.audience.removeAudience)
      .get("button")
      .contains("Yes, delete it")
      .eq(0)
      .click()
  })
})
