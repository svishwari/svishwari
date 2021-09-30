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
    //click on engagement on side nav bar and route in engagement screen
    cy.get(selector.engagements).click()
    cy.location("pathname").should("eq", route.engagements)
    //click over the first engagement name
    cy.get("a[href='/engagements/2']").click()
   // cy.get(selector.engagement.engagementCollection.eq(0).find('div.d-flex > button > a')).click()
  })

  it("should be able to view the engagement dashboard overview", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    //click on engagement on side nav bar and route in engagement screen
    cy.get(selector.engagements).click()
    cy.location("pathname").should("eq", route.engagements)
    //click on add engagement button
    cy.get("a[href='/engagements/2']").click()
   // cy.get(selector.engagement.engagementCollection.eq(0).find('div.d-flex > button > a')).click()
  })

  it("should be able to view the audiences", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    //click on engagement on side nav bar and route in engagement screen
    cy.get(selector.engagements).click()
    cy.location("pathname").should("eq", route.engagements)
    //click on add engagement button
    cy.get("a[href='/engagements/2']").click()
   // cy.get(selector.engagement.engagementCollection.eq(0).find('div.d-flex > button > a')).click()
  })

  it("should be able to view the audiences", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    //click on engagement on side nav bar and route in engagement screen
    cy.get(selector.engagements).click()
    cy.location("pathname").should("eq", route.engagements)
    //click on add engagement button
    cy.get("a[href='/engagements/2']").click()
   // cy.get(selector.engagement.engagementCollection.eq(0).find('div.d-flex > button > a')).click()
  })

  it("should be able to validate the delivery history", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    //click on engagement on side nav bar and route in engagement screen
    cy.get(selector.engagements).click()
    cy.location("pathname").should("eq", route.engagements)
    //click on add engagement button
    cy.get("a[href='/engagements/2']").click()
   // cy.get(selector.engagement.engagementCollection.eq(0).find('div.d-flex > button > a')).click()
  })

  it("should be able to validate the audience performance data for digital advertising", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    //click on engagement on side nav bar and route in engagement screen
    cy.get(selector.engagements).click()
    cy.location("pathname").should("eq", route.engagements)
    //click on add engagement button
    cy.get("a[href='/engagements/2']").click()
   // cy.get(selector.engagement.engagementCollection.eq(0).find('div.d-flex > button > a')).click()
  })

  it("should be able to validate the audience performance data for email marketing", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)
    //click on engagement on side nav bar and route in engagement screen
    cy.get(selector.engagements).click()
    cy.location("pathname").should("eq", route.engagements)
    //click on add engagement button
    cy.get("a[href='/engagements/2']").click()
   // cy.get(selector.engagement.engagementCollection.eq(0).find('div.d-flex > button > a')).click()
  })
})
