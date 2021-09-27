import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Data management > Customer Profiles", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to view the overview", () => {
    cy.location("pathname").should("eq", route.overview)

    //click on customer profiles on side nav bar
    cy.get(selector.customerProfile.customers).click()
    cy.location("pathname").should("eq", route.customerProfiles)
  })

  it("should be able to view overview of customer profiles", () => {
    //validate overview exist by getting total no. of them
    cy.get(selector.customerProfile.overview).its("length").as("overviewListCount")
    cy.get("@overviewListCount").then(() => {
      cy.get(selector.customerProfile.overview).its("length").should("eq", 8)
    })
  })

  it("should be able to view customer overview of customer profiles", () => {
    //validate customer overview exist by getting total no. of them
    cy.get(selector.customerProfile.customeroverview).its("length").as("customeroverviewListCount")
    cy.get("@customeroverviewListCount").then(() => {
      cy.get(selector.customerProfile.customeroverview).its("length").should("eq", 8)
    })
  })

})
