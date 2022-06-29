import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Data management > Customer Profiles", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.customerProfiles)
  })

  it("should have an Overview, Total customers, Geographic and Demographic charts", () => {
    cy.location("pathname").should("eq", route.customerProfiles)

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    // should be able to view customer overview of customer profiles"
    cy.get(selector.customerProfile.customeroverview)
      .its("length")
      .as("customeroverviewListCount")

    cy.get("@customeroverviewListCount").then(() => {
      cy.get(selector.customerProfile.customeroverview)
        .its("length")
        .should("eq", 6)
    })

    // Verifying the table columns names of the Country Drawer
    const tableHeadersCountry = ["Country", "Size", "Avg. spend"]

    cy.get(selector.customerProfile.customeroverview).eq(1).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)

    cy.get(selector.customerProfile.list.geoDrawerTableCountry)
      .find(selector.customerProfile.list.geoDrawerTableHeaders)
      .children()
      .each(($elm, i) => {
        expect($elm.text()).equal(tableHeadersCountry[i])
      })

    cy.get(selector.customerProfile.list.geoDrawerTableCountry)
      .find(selector.customerProfile.list.geoDrawerTableItems)
      .children()
      .its("length")
      .should("be.gt", 0)

    cy.get(selector.engagement.exitDrawer).click()

    // Verifying the table columns names of the State Drawer
    const tableHeadersStateMultipleCountries = [
      "State",
      "Country",
      "Size",
      "Avg. spend",
    ]
    const tableHeadersState = ["State", "Size", "Avg. spend"]

    cy.get(selector.customerProfile.customeroverview).eq(2).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    cy.get(selector.customerProfile.list.geoDrawerTableState)
      .find(selector.customerProfile.list.geoDrawerTableHeaders)
      .children()
      .each(($elm, i, $lis) => {
        if ($lis.length == tableHeadersStateMultipleCountries.length) {
          expect($elm.text()).equal(tableHeadersStateMultipleCountries[i])
        } else {
          expect($elm.text()).equal(tableHeadersState[i])
        }
      })

    cy.get(selector.customerProfile.list.geoDrawerTableState)
      .find(selector.customerProfile.list.geoDrawerTableItems)
      .children()
      .its("length")
      .should("be.gt", 0)

    cy.get(selector.engagement.exitDrawer).click()

    // Verifying the table columns names of the Cities Drawer
    const tableHeadersCitiesMultipleCountries = [
      "City",
      "State",
      "Country",
      "Size",
      "Avg. spend",
    ]
    const tableHeadersCities = ["City", "State", "Size", "Avg. spend"]

    cy.get(selector.customerProfile.customeroverview).eq(3).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    cy.get(selector.customerProfile.list.geoDrawerTableCity)
      .find(selector.customerProfile.list.geoDrawerTableHeaders)
      .children()
      .each(($elm, i, $lis) => {
        if ($lis.length == tableHeadersCitiesMultipleCountries.length) {
          expect($elm.text()).equal(tableHeadersCitiesMultipleCountries[i])
        } else {
          expect($elm.text()).equal(tableHeadersCities[i])
        }
      })

    cy.get(selector.customerProfile.list.geoDrawerTableCity)
      .find(selector.customerProfile.list.geoDrawerTableItems)
      .children()
      .its("length")
      .should("be.gt", 0)

    cy.get(selector.engagement.exitDrawer).click()

    //IDR drawer click
    cy.get(selector.customerProfile.customerIdrDrawer).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.engagement.exitDrawer).click()
    // should be able to check if valid response for total customers has received"
    cy.get(selector.customerProfile.totalCustomerchart)
      .its("length")
      .should("gt", 0)

    // should be able to check if valid response for customers spend has received"
    cy.get(selector.customerProfile.customerSpendchart)
      .its("length")
      .should("gt", 0)

    // should be able to hover over state"
    cy.get(".geochart")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // map state list should have a list of states"
    cy.get(selector.customerProfile.mapStateList)
      .its("length")
      .should("be.gt", 0)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    // click on customer list tab
    cy.get(selector.customerProfile.customerListTab).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    // scroll down for lazy loading
    cy.get(".content-section").scrollTo("bottom", { ensureScrollable: true })
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
  })
})
