import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Orchestration > Engagement > Engagement Dashboard", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to navigate to engagement and select one of the engagement", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    // click on engagement on side nav bar and route in engagement screen
    cy.get(selector.engagements).click()
    cy.location("pathname").should("eq", route.engagements)
    //click over the first engagement name and navigate to engagement dashboard 
    cy.get(selector.engagement.engagementList).eq(0).find("a").should('have.attr', 'href')
    .then((href) => {
      cy.visit(href)
    })
  })

  it("should be able to view the engagement dashboard overview", () => {
    // check if overview cards don't contain empty value
    cy.get(selector.engagement.overviewSummary).should(($overview) => {
        expect($overview.find(selector.engagement.deliveryScheduleMetric)).to.not.equal('-')
        expect($overview.find(selector.engagement.updatedMetric)).to.not.equal('-')
        expect($overview.find(selector.engagement.createdMetric)).to.not.equal('-')
     })
  })

  it("should be able to view the audiences", () => {
    // Validate if there is/are audience(s) attached to current enagagement
    cy.get(selector.engagement.engagementAudienceList).its("length").should("gt", 0)
  })

  it("should be able to view the delivery history", () => {
    // Click on delivery history link and open drawer
    cy.get(selector.engagement.deliveryHistory).click()
    // Validate if the table has got valid items
    cy.get(selector.engagement.deliveryHistoryItems).its("length").should("gt", 0)
    // Close the delivery history drawer
    cy.get(selector.engagement.exitDrawer).click()
  })

  it("should be able to view the audience performance data for digital advertising", () => {
    // By default Digital Advertising tab is active
    cy.get(selector.engagement.audiencePerformance).its("length").should("gt", 0)
  })

  it("should be able to view the audience performance data for email marketing", () => {
    // click on Email Marketing tab
    cy.get(selector.engagement.emailMarketing).click()
    cy.get(selector.engagement.emailData).its("length").should("gt", 0)
  })
})
