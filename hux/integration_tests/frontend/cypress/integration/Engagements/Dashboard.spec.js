import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Orchestration > Engagement > Engagement Dashboard", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to navigate to engagement dashobard and verify it", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    // click on engagement on side nav bar and route in engagement screen
    cy.get(selector.nav.engagements).click()
    cy.location("pathname").should("eq", route.engagements)

    // click over the engagement name that has active status with more than 1 audience and navigate to dashboard
    cy.get(selector.engagement.activeEngagement)
      .first()
      .find("a")
      .should("have.attr", "href")
      .then((href) => {
        cy.visit(href)
      })

    // it should be able to view the engagement dashboard overview
    cy.get(selector.engagement.deliveryScheduleMetric).should("exist")
    cy.get(selector.engagement.updatedMetric)
      .should("exist")
      .and("contain", "ago by")
    cy.get(selector.engagement.createdMetric)
      .should("exist")
      .and("contain", "ago by")

    // it should be able to view the audiences
    cy.get(selector.engagement.engagementAudienceList)
      .its("length")
      .should("gt", 0)

    // it should be able to view the delivery history
    // Click on delivery history link and open drawer
    cy.get(selector.engagement.deliveryHistory).click()
    // Validate if the table has got valid items
    cy.get(selector.engagement.deliveryHistoryItems)
      .its("length")
      .should("gt", 0)
    // Close the delivery history drawer
    cy.get(selector.engagement.exitDrawer).click()

    // it should be able to view the audience performance data for digital advertising
    cy.get(selector.engagement.adsData).its("length").should("gt", 0)

    // it should be able to view the audience performance data for email marketing
    cy.get(selector.engagement.emailMarketing).click()
    cy.get(selector.engagement.emailData).its("length").should("gt", 0)
  })
})
