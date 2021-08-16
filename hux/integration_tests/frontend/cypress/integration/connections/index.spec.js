import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Tests data souces and destinations in connections", () => {
  before(() => {
    // opens the app
    cy.visit(route.home)

    // clicks the signin button
    cy.get(selector.home.signin).click()

    // we should now be on the login page
    cy.location("pathname").should("eq", route.login)

    // fill in the form
    cy.get(selector.login.email).type(Cypress.env("USER_EMAIL"), { log: false })

    cy.get(selector.login.password).type(Cypress.env("USER_PASSWORD"), {
      log: false,
    })

    // submit the form
    cy.get(selector.login.submit).click()

    // TODO: add MFA related authentication if needed

    // we should no longer be on the login page
    cy.location("pathname", { timeout: 10000 })
      .should("not.eq", route.login)
      .then(() => {
        // okta does its authentication...
        // once its done, we should be redirected back to the app
        cy.location("pathname").should("eq", route.oktaSignInRedirectURI)
      })
  })

  it("testing data management > connections > data sources", () => {
    cy.location("pathname").should("eq", route.overview)

    //click on connections on side nav bar
    cy.get(selector.connections).click()
    cy.location("pathname").should("eq", route.connections)

    //validate data sources exist by getting total no. of them
    cy.get(selector.datasources).its("length").as("dataSourcesCount")

    //add a data source
    cy.get(selector.addDataSource).click()
    cy.location("pathname").should("eq", route.addDataSource)
    cy.get(selector.dataSourcesAdd).eq(0).click()
    cy.get("button").contains("Add 1 data source").click()
    cy.location("pathname").should("eq", route.connections)

    // TODO: improve waiting for the data source list to load
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    //make sure that number of data sources have increased by 1
    cy.get("@dataSourcesCount").then((dataSourcesCount) => {
      cy.get(selector.datasources)
        .its("length")
        .should("eq", dataSourcesCount + 1)

      //validate correct status on all added data sources
      cy.get(selector.datasources).as("dataSourcesList")
      for (let index = 0; index < dataSourcesCount; index++) {
        cy.get("@dataSourcesList").eq(index).contains("Active")
      }
      cy.get("@dataSourcesList").eq(dataSourcesCount).contains("Pending")
    })
  })

  it("testing data management > connections > destinations", () => {
    cy.location("pathname").should("eq", route.connections)
    cy.get(selector.destinations).its("length").should("be.gt", 0)
  })
})
