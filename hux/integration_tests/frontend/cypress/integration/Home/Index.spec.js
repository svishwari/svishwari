import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("View Overview", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to login into UI and view welcome banner", () => {
    let currentUser = {}
    cy.location("pathname").should("eq", route.overview)
    cy.window().then((window) => {
      currentUser = JSON.parse(window.localStorage.getItem("vuex")).users
        .userProfile
      cy.get(selector.card.title).contains(
        currentUser.firstName + " " + currentUser.lastName,
      )
    })
  })

  it("should be able to view configuration action items", () => {
    cy.get(selector.overview.item).should(($overview) => {
      expect($overview).to.have.length(4)

      // Connect Data source action
      expect($overview.eq(0).find(selector.card.title)).to.contain(
        "Connect data source",
      )
      expect($overview.eq(0).find(selector.card.description)).to.contain(
        "Connect your data sources to enable data unification in a single location.",
      )
      expect($overview.eq(0).prop("href")).to.contain(route.dataSources)

      // Add Destination action
      expect($overview.eq(1).find(selector.card.title)).to.contain(
        "Add a destination",
      )
      expect($overview.eq(1).find(selector.card.description)).to.contain(
        "Select the destinations you wish to deliver your audiences and/or engagements to.",
      )
      expect($overview.eq(1).prop("href")).to.contain(route.destinations)

      // Add Audience action
      expect($overview.eq(2).find(selector.card.title)).to.contain(
        "Create an audience",
      )
      expect($overview.eq(2).find(selector.card.description)).to.contain(
        "Create audiences by segmenting your customer list based on who you wish to target.",
      )
      expect($overview.eq(2).prop("href")).to.contain(route.audiences)

      // Add Engagement action
      expect($overview.eq(3).find(selector.card.title)).to.contain(
        "Create an engagement",
      )
      expect($overview.eq(3).find(selector.card.description)).to.contain(
        "Select your audiences and destinations where you wish to run campaigns on.",
      )
      expect($overview.eq(3).prop("href")).to.contain(route.engagements)
    })
  })

  it("should be able to check if valid response for total customers has received", () => {
    //validate Total Customer response
    cy.get(selector.overview.chart).its("length").should("gt", 0)
  })
})
