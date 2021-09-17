import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Tests overview in Identity Resolution", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("testing data management >  identity resolution", () => {
    cy.location("pathname").should("eq", route.overview)

    //click on identity resolution on side nav bar
    cy.get(selector.identityResolution).click()
    cy.location("pathname").should("eq", route.identityResolution)

  })

  it("testing data management >  identity resolution > overview", () => {

    //validate overview exist by getting total no. of them
    cy.get(selector.overview).its("length").as("overviewListCount")
    cy.get("@overviewListCount").then((overviewListCount) => {
        cy.get(selector.overview).its("length").should("eq", overviewListCount)
    })

  })

  it("testing data management >  identity resolution > data feed", () => {

    //validate data feed
    cy.get(selector.datafeed).its("length").as("datafeedListCount")
    cy.get("@datafeedListCount").then((datafeedListCount) => {
        cy.get(selector.datafeed).its("length").should("eq", datafeedListCount)
    })

  })
})
