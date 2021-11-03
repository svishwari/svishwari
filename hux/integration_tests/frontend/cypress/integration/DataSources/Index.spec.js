import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Data Management > Data Sources", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.dataSources)
  })

  it("should be able to manage data sources", () => {
    cy.location("pathname").should("eq", route.dataSources)

    // validate data sources exist by getting total no. of them
    let dataSourceAddCount = 0
    cy.get(selector.dataSourcesAdd).then(($ele) => {
      dataSourceAddCount = $ele.length
    })

    cy.get(selector.datasources).then(($elem) => {
      // add a data source
      cy.get(selector.addDataSource).click()
      cy.get(selector.dataSourcesRequest).each(($el) => {
        if (!$el.attr("class").includes("v-card--disabled")) {
          cy.wrap($el).click()
          return false
        }
      })
      cy.get("button").contains("Request 1 data source").click()
      cy.location("pathname").should("eq", route.dataSources)

      // TODO: improve waiting for the data source list to load
      // eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(1000)

      // make sure that number of data sources have increased by 1
      cy.get(selector.datasources)
        .its("length")
        .should("eq", $elem.length + 1)

      cy.get(selector.pendingStatus)
        .eq(0)
        .siblings(".mdi-dots-vertical")
        .click()
      cy.get(selector.pendingDataSourceRemove).eq(0).click()
      cy.get(selector.removeDataSourceConfirmation)
        .get("button")
        .contains("Yes, remove it")
        .eq(0)
        .click()

      cy.get(selector.engagement.exitDrawer).click()
    })
  })

  it("should be able to quick-add a data source from the top nav", () => {
    cy.get(selector.nav.dataSources).eq(0).click()
    cy.location("pathname").should("eq", route.dataSources)

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
