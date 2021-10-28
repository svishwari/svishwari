import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Data Management > Data Sources", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  // TODO in HUS-1373 after HUS-1230 is merged
  it.skip("should be able to manage data sources", () => {
    cy.location("pathname").should("eq", route.home)

    // click on connections on side nav bar
    cy.get(selector.nav.dataSources).click()
    cy.location("pathname").should("eq", route.dataSources)

    // validate data sources exist by getting total no. of them
    let dataSourceAddCount = 0
    cy.get(selector.dataSourcesAdd).then(($ele) => {
      dataSourceAddCount = $ele.length
    })

    cy.get(selector.datasources).then(($elem) => {
      if ($elem.length != dataSourceAddCount) {
        // add a data source
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

        // make sure that number of data sources have increased by 1
        cy.get(selector.datasources)
          .its("length")
          .should("eq", $elem.length + 1)

        // validate correct status on all added data sources
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

  // TODO in HUS-1373 after HUS-1230 is merged
  it.skip("should be able to quick-add a data source from the top nav", () => {
    cy.get(selector.connections).eq(0).click()
    cy.location("pathname").should("eq", route.connections)

    // click on add button on nav bar header
    cy.get(selector.datasources).should("exist")
    cy.get(selector.topNav.add).eq(0).click()

    // open data source drawer
    cy.get(selector.topNav.dataSourceButton).eq(0).click()

    // validate the drawer is open
    cy.get(selector.dataSourcesAdd).its("length").should("be.gt", 0)

    cy.get(selector.engagement.exitDrawer).click()
  })
})
