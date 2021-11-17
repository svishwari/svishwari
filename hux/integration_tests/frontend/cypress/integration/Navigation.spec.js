import route from "../support/routes.js"
import selector from "../support/selectors.js"

describe("Navigation", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.home)
  })

  it("should be able to navigate to all sections", () => {
    // home
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.nav.home).click()
    cy.location("pathname").should("eq", route.home)

    // data sources
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.nav.dataSources).click()
    cy.location("pathname").should("eq", route.dataSources)

    // identity resolution
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.nav.identityResolution).click()
    cy.location("pathname").should("eq", route.identityResolution)

    // models
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    //cy.wait(1000)
    // cy.get(selector.nav.models).click()
    // cy.location("pathname").should("eq", route.models)

    // customer profiles
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.nav.customerProfiles).click()
    cy.location("pathname").should("eq", route.customerProfiles)

    // segment playground
    // cy.get(selector.nav.segmentPlayground).should("exist")

    // destinations
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.nav.destinations).click()
    cy.location("pathname").should("eq", route.destinations)

    // audiences
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.nav.audiences).click()
    cy.location("pathname").should("eq", route.audiences)

    // engagements
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.nav.engagements).click()
    cy.location("pathname").should("eq", route.engagements)

    // help
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.topNav.help).click()

    // contact us
    // cy.get(selector.topNav.contactus)
    //   .find("a")
    //   .should("have.attr", "href")
    //   .and("include", "mailto")

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
