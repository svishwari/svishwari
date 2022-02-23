import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Orchestration > Engagement > Engagement Dashboard", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.engagements)
  })

  it("should be able to view an engagement's dashboard", () => {
    cy.location("pathname").should("eq", route.engagements)

    cy.get(".menu-cell-wrapper")
      .first()
      .find("a")
      .should("have.attr", "href")
      .then((href) => {
        cy.visit(href)
      })
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
    cy.get(selector.engagement.engagementTabs).its("length").should("gt", 0)

    //overview tab
    if (cy.get(selector.engagement.engagementTabs).contains("Overview")) {
      cy.get(selector.engagement.overviewMetrics).should("exist")

      // it should be able to view the delivery history
      // Click on delivery history link and open drawer
      cy.get(selector.engagement.deliveryHistory).click()
      // Validate if the table has got valid items
      cy.get(selector.engagement.deliveryHistoryItems)
        .its("length")
        .should("gte", 0)
      // Close the delivery history drawer
      cy.get(selector.engagement.exitDrawer).click()
      cy.get(selector.engagement.overviewAudiences).should("exist")
    }

    // digital advertising tab
    if (
      cy.get(selector.engagement.engagementTabs).contains("Digital Advertising")
    ) {
      cy.get(selector.engagement.engagementTabs)
        .contains("Digital Advertising")
        .click()

      //eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(3000)
      cy.get(selector.engagement.advertisingOverview).should("exist")
      // it should be able to view the audience performance data for digital advertising
      cy.get(selector.engagement.adsData).its("length").should("exist")
      cy.get(selector.engagement.accessActions).eq(0).click()
      cy.get(selector.engagement.actions).contains("Open destination")
      cy.get(selector.engagement.actions).contains("Edit delivery schedule")
      cy.get(selector.engagement.actions).contains("Remove destination")
    }

    // email marketing tab
    if (
      cy.get(selector.engagement.engagementTabs).contains("Email Marketing")
    ) {
      cy.get(selector.engagement.engagementTabs)
        .contains("Email Marketing")
        .click()

      //eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(3000)
      cy.get(selector.engagement.emailOverview).should("exist")
      // it should be able to view the audience performance data for digital advertising
      cy.get(selector.engagement.emailData).its("length").should("exist")
    }
  })
})
