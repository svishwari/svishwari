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
    cy.get(selector.datasource.dataSourcesAdd).its("length").should("be.gt", 0)

    cy.get(selector.datasource.datasources).then(($elem) => {
      // add a data source
      cy.get(selector.datasource.addDataSource).click()
      cy.get(selector.datasource.dataSourcesRequest).each(($el) => {
        if (!$el.attr("class").includes("v-card--disabled")) {
          cy.wrap($el).click()
          return false
        }
      })
      cy.get("button").contains("Cancel")
      cy.get("button").contains("Request 1 data source").click()
      cy.location("pathname").should("eq", route.dataSources)

      // eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(4000)

      cy.get(selector.datasource.datasources)
        .its("length")
        .should("eq", $elem.length + 1)

      cy.get(selector.datasource.pendingStatus)
        .eq(0)
        .siblings(".mdi-dots-vertical")
        .click()
      cy.get(selector.datasource.pendingDataSourceRemove).eq(0).click()
      cy.get(selector.datasource.removeDataSourceConfirmation)
        .get("button")
        .contains("Nevermind")
      cy.get(selector.datasource.removeDataSourceConfirmation)
        .get("button")
        .contains("Yes, remove it")
        .click()

      cy.get(selector.engagement.exitDrawer).click()
    })
  })

  it("should be able to quick-add a data source from the top nav", () => {
    cy.get(selector.nav.dataSources).eq(0).click()
    cy.location("pathname").should("eq", route.dataSources)

    // click on add button on nav bar header
    cy.get(selector.datasource.datasources).should("exist")
    cy.get(selector.topNav.add).eq(0).click()

    // open data source drawer
    cy.get(selector.topNav.dataSourceButton).eq(0).click()

    // validate the drawer is open
    cy.get(selector.datasource.dataSourcesAdd).its("length").should("be.gt", 0)

    cy.get(selector.engagement.exitDrawer).click()
  })

  it("should be able to open data feeds table", () => {
    cy.get(selector.nav.dataSources).eq(0).click()
    cy.location("pathname").should("eq", route.dataSources)

    // click on add button on nav bar header
    cy.get(selector.datasource.datasources).should("exist")
    cy.get(selector.datasource.datasources).eq(0).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(4000)
    cy.get(selector.datasource.datasourceDatafeedsTable).then((datafeeds) => {
      if (datafeeds.find(".data-feed-name").length > 0) {
        datafeeds.find(".data-feed-name").eq(0).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(4000)
        cy.get(selector.datasource.dataFilesWrapper).then((elem) => {
          if (elem.find(".datasource-datafeeds-details-table").length > 0) {
            cy.get(selector.datasource.dataFeedDetailsTable).should("exist")
            cy.get(selector.datasource.datasourceGroupedFilesExpand)
              .eq(0)
              .click()
            cy.get(selector.datasource.datasourceFilesStatus)
              .eq(0)
              .trigger("mouseover", { force: true })

            cy.get(selector.datasource.datasourceFilesTableFilter).should(
              "exist",
            )
            cy.get(selector.datasource.datasourceFilesTableFilter).eq(0).click()
            cy.get(selector.datasource.datasourceFilesTableFilterDrawer).should(
              "exist",
            )
            cy.get(
              selector.datasource.datasourceFilesTableFilterDrawerTimePanel,
            )
              .eq(0)
              .click()

            cy.get(
              selector.datasource
                .datasourceFilesTableFilterDrawerTimePanelToday,
            )
              .eq(0)
              .click({ force: true })
            cy.get(selector.filter.apply).eq(0).click()
            cy.get(selector.datasource.datasourceFilesTableFilter).eq(0).click()

            cy.get(
              selector.datasource
                .datasourceFilesTableFilterDrawerTimePanelYesterday,
            )
              .eq(0)
              .click({ force: true })
            cy.get(selector.filter.apply).eq(0).click()
            cy.get(selector.datasource.datasourceFilesTableFilter).eq(0).click()

            cy.get(
              selector.datasource
                .datasourceFilesTableFilterDrawerTimePanelToday,
            )
              .eq(0)
              .click({ force: true })
            cy.get(selector.filter.apply).eq(0).click()
            cy.get(selector.datasource.datasourceFilesTableFilter).eq(0).click()

            cy.get("input[value='Last week']").eq(0).click({ force: true })
            cy.get(selector.filter.apply).eq(0).click()
            cy.get(selector.datasource.datasourceFilesTableFilter).eq(0).click()

            cy.get("input[value='Last month']").eq(0).click({ force: true })
            cy.get(selector.filter.apply).eq(0).click()
            cy.get(selector.datasource.datasourceFilesTableFilter).eq(0).click()

            cy.get("input[value='All time']").eq(0).click({ force: true })
            cy.get(selector.filter.apply).eq(0).click()
            cy.get(selector.datasource.datasourceFilesTableFilter).eq(0).click()

            cy.get(selector.filter.clear).eq(0).click()
            cy.get(selector.filter.close).eq(0).click()
          } else {
            cy.wrap(elem.find(".empty-error-card")).should("exist")
          }
        })
      }
    })
  })
})
