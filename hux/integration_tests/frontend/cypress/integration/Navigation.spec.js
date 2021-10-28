import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Navigation", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to navigate to all sections", () => {
    // home
    cy.get(selector.nav.home).click()
    cy.location("pathname").should("eq", route.home)

    // configuration
    cy.get(selector.nav.configuration).click()
    cy.location("pathname").should("eq", route.configuration)

    // data sources
    cy.get(selector.nav.dataSources).click()
    cy.location("pathname").should("eq", route.dataSources)

    // identity resolution
    cy.get(selector.nav.identityResolution).click()
    cy.location("pathname").should("eq", route.identityResolution)

    // models
    cy.get(selector.nav.models).click()
    cy.location("pathname").should("eq", route.models)

    // customer profiles
    cy.get(selector.nav.customerProfiles).click()
    cy.location("pathname").should("eq", route.customerProfiles)

    // segment playground
    cy.get(selector.nav.segmentPlayground).should("exist")

    // destinations
    cy.get(selector.nav.destinations).click()
    cy.location("pathname").should("eq", route.destinations)

    // audiences
    cy.get(selector.nav.audiences).click()
    cy.location("pathname").should("eq", route.audiences)

    // engagements
    cy.get(selector.nav.engagements).click()
    cy.location("pathname").should("eq", route.engagements)

    // help
    cy.get(selector.topNav.help).click()

    // contact us
    cy.get(selector.topNav.contactus)
      .find("a")
      .should("have.attr", "href")
      .and("include", "mailto")

    // quick add: data source, destination, audience, engagement
    cy.get(selector.topNav.add).click()

    // user profile: my profile, logout
    cy.get(selector.topNav.profiledropdown).click()
    cy.get(selector.topNav.profile)
      .should("have.attr", "href")
      .and("include", "okta.com")
    cy.get(selector.topNav.logout).click()
  })
})
