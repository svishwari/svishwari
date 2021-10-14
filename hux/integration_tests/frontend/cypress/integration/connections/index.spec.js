import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Tests data sources and destinations in connections", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("testing data management > connections > data sources", () => {
    cy.location("pathname").should("eq", route.overview)

    //click on connections on side nav bar
    cy.get(selector.connections).eq(0).click()
    cy.location("pathname").should("eq", route.connections)

    //validate data sources exist by getting total no. of them
    let dataSourceAddCount = 0
    cy.get(selector.dataSourcesAdd).then(($ele) => {
      dataSourceAddCount = $ele.length
    })

    cy.get(selector.datasources).then(($elem) => {
      if ($elem.length != dataSourceAddCount) {
        //add a data source
        cy.get(selector.addDataSource).click()
        cy.get(selector.dataSourcesAdd).each(($el) => {
          if (!$el.attr("class").includes("v-card--disabled")) {
            cy.wrap($el).click()
            return false
          }
        })
        cy.get("button").contains("Add 1 data source").click()
        cy.location("pathname").should("eq", route.connections)

        // TODO: improve waiting for the data source list to load
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)

        //make sure that number of data sources have increased by 1
        cy.get(selector.datasources)
          .its("length")
          .should("eq", $elem.length + 1)

        //validate correct status on all added data sources
        cy.get(selector.datasources).as("dataSourcesList")
        for (let index = 0; index < $elem.length; index++) {
          cy.get("@dataSourcesList")
            .eq(index)
            .contains(/Active|Pending/)
        }

        cy.get(selector.engagement.exitDrawer).click()
      } else {
        cy.get(selector.pendingDataSource).eq(0).click()
        cy.get(selector.pendingDataSourceRemove).eq(0).click()
        cy.get(selector.removeDataSourceConfirmation)
          .get("button")
          .contains("Yes, remove it")
          .eq(0)
          .click()
        cy.wait(2000)
        cy.get(selector.datasources).then(($elem) => {
          if ($elem.length != dataSourceAddCount) {
            //add a data source
            cy.get(selector.addDataSource).click()
            cy.get(selector.dataSourcesAdd).each(($el) => {
              if (!$el.attr("class").includes("v-card--disabled")) {
                cy.wrap($el).click()
                return false
              }
            })
            cy.get("button").contains("Add 1 data source").click()
            cy.location("pathname").should("eq", route.connections)

            // TODO: improve waiting for the data source list to load
            // eslint-disable-next-line cypress/no-unnecessary-waiting
            cy.wait(1000)

            //make sure that number of data sources have increased by 1
            cy.get(selector.datasources)
              .its("length")
              .should("eq", $elem.length + 1)

            //validate correct status on all added data sources
            cy.get(selector.datasources).as("dataSourcesList")
            for (let index = 0; index < $elem.length; index++) {
              cy.get("@dataSourcesList")
                .eq(index)
                .contains(/Active|Pending/)
            }

            cy.get(selector.engagement.exitDrawer).click()
          }
        })
      }
    })
  })

  it("testing data management > connections > destinations", () => {
    cy.get(selector.connections).eq(0).click()
    cy.location("pathname").should("eq", route.connections)
    cy.get(selector.destinations).its("length").should("be.gt", 0)
  })

  it("testing data management > connections > add data sources from navbar", () => {
    cy.get(selector.connections).eq(0).click()
    cy.location("pathname").should("eq", route.connections)

    //click on add button on nav bar header
    cy.get(selector.datasources).should("exist")
    cy.get(selector.navigation.add).eq(0).click()

    //open data source drawer
    cy.get(selector.navigation.dataSourceButton).eq(0).click()

    //validate the drawer is open
    cy.get(selector.dataSourcesAdd).its("length").should("be.gt", 0)

    cy.get(selector.engagement.exitDrawer).click()
  })
})
