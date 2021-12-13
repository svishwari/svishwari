import route from "../../support/routes"
import selector from "../../support/selectors"
import { randomName } from "../../support/utils"

let randomAudienceName = randomName()

describe("Orchestration > Audience > Create Audience", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.audiences)
    cy.wait(3000)
  })

  it.skip("should be able to configure a new audience", () => {
    cy.location("pathname").should("eq", route.audiences)
    //click on add audience button
    cy.get(selector.audience.addAudiences).eq(0).click()

    // click on Save as an audience
    cy.get(selector.audience.actionAudience).click()

    // should fill new audience name and description
    // add new audience name
    cy.get(selector.audience.audienceName)
      .eq(0)
      .type(`E2E test audience ${randomAudienceName}`)

    // should add the destination to the audience
    // Click on add audience icon
    cy.contains("Save").click()
    // cy.get(selector.audience.removeAudience).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)

    cy.get("body").then(($body) => {
      if ($body.find(selector.audience.selectEngagement).length > 0) {
        // Select the first audience from the existing ones
        cy.get(selector.audience.selectEngagement).eq(0).click()
      } else if ($body.find(selector.audience.newEngagementFirst).length > 0) {
        cy.get(selector.audience.newEngagementFirst).click()
        cy.get(selector.audience.newEngagementFirstName)
          .eq(0)
          .type(`E2E test engagement ${randomAudienceName}`)
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
          .type(`New Data Extension Text ${randomAudienceName}`)
        // Close the data extension drawer
        cy.get(selector.engagement.exitDataExtensionDrawer).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)
      }
    })

    // Close the add destination drawer
    cy.get(selector.engagement.exitDrawer).click()

    // TODO: skipping creating an audience until local miragejs issue is resolved
    cy.get(selector.audience.createAudience).click()
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(10000)
    cy.location("pathname").should("contain", "insight")
  })

  // This test case is written to delete an audience created above
  it.skip("should be able to delete a newly added audience", () => {
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)

    cy.get(".menu-cell-wrapper").each(($el) => {
      if ($el.text().includes(`E2E test audience ${randomAudienceName}`)) {
        // Make the vertical dots visible
        cy.wrap($el)
          .find(".mdi-dots-vertical")
          .invoke("attr", "aria-expanded", "true")
          .click({ force: true })

        cy.contains("Delete audience").click()
        cy.contains("Yes, delete it").click()
        //eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(2000)
      }
    })
  })
})
