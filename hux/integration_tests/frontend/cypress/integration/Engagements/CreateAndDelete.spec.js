import route from "../../support/routes.js"
import selector from "../../support/selectors.js"
import { randomName } from "../../support/utils"

let engagementName = randomName()

describe("Orchestration > Engagement > Create Engagement", () => {
  beforeEach(() => {
    cy.signin()
  })

  it("should be able to configure a new engagement", () => {
    cy.visit(route.addEngagement)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
    // should fill new engagement name and description
    // add new engagement name
    cy.get(selector.engagement.enagagementName)
      .eq(0)
      .type(`Test Engagement ${engagementName}`)
    // add new engagement description
    cy.get(selector.engagement.enagagementDescription)
      .eq(0)
      .type("Engagement for E2E testing")

    // should add audience to the engagement
    // Click on add audience icon
    cy.get(selector.engagement.addAudience).click()
    // Select the first audience from the existing ones
    cy.get(selector.engagement.selectAudience).eq(0).click()
    // Click on outside the close the add audience Drawer
    cy.get(selector.engagement.exitDrawer).click()

    // should add destination to the engagement
    // Click on add audience icon
    cy.get(selector.engagement.addDestination).click()
    // Select the first destination from the existing ones
    cy.get(selector.engagement.selectDestination).eq(0).click()
    cy.get(selector.engagement.exitDrawer).click()

    // add a check that it requires data extension name before proceeding
    cy.get(selector.engagement.addDestination).click()
    cy.get("body").then(($body) => {
      if ($body.find(selector.engagement.salesForceAddButton).length > 0) {
        cy.get(selector.engagement.salesForceAddButton).click()
        // Add new data extension name
        cy.get(selector.engagement.dataExtensionName)
          .eq(1)
          .type(`Test Engagement ${engagementName}`)
        // Close the data extension drawer
        cy.get(selector.engagement.exitDataExtensionDrawer).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)
        // Close the add destination drawer
        cy.get(selector.engagement.exitDrawer).click()
      }
    })

    // create engagement
    cy.get(selector.engagement.createEngagement).click()
  })

  // This test case is written to delete an engagement created above
  it("should be able to delete a newly added engagement", () => {
    cy.visit(route.engagements)

    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)

    cy.get(".menu-cell-wrapper").each(($el) => {
      if ($el.text().includes(`Test Engagement ${engagementName}`)) {
        // Make the vertical dots visible
        cy.wrap($el)
          .find(".mdi-dots-vertical")
          .invoke("attr", "aria-expanded", "true")
          .click({ force: true })

        cy.contains("Delete engagement").click()
        cy.contains("Yes, delete engagement").click()
        //eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(2000)
      }
    })
  })
})
