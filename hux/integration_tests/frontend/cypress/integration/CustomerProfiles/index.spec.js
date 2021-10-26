import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Data management > Customer Profiles", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should have an Overview, Total customers, Geographic and Demographic charts", () => {
    cy.location("pathname").should("eq", route.overview)

    // click on customer profiles on side nav bar
    cy.get(selector.customerProfile.customers).click()
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
    const tableHeadersCountry = ["Country", "Size", "Spending $"]

    cy.get(selector.customerProfile.customeroverview).eq(1).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

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
    const tableHeadersState = ["State", "Country", "Size", "Spending $"]

    cy.get(selector.customerProfile.customeroverview).eq(2).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    cy.get(selector.customerProfile.list.geoDrawerTableState)
      .find(selector.customerProfile.list.geoDrawerTableHeaders)
      .children()
      .each(($elm, i) => {
        expect($elm.text()).equal(tableHeadersState[i])
      })

    cy.get(selector.customerProfile.list.geoDrawerTableState)
      .find(selector.customerProfile.list.geoDrawerTableItems)
      .children()
      .its("length")
      .should("be.gt", 0)

    cy.get(selector.engagement.exitDrawer).click()

    // Verifying the table columns names of the Cities Drawer
    const tableHeadersCities = [
      "City",
      "State",
      "Country",
      "Size",
      "Spending $",
    ]

    cy.get(selector.customerProfile.customeroverview).eq(3).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    cy.get(selector.customerProfile.list.geoDrawerTableCity)
      .find(selector.customerProfile.list.geoDrawerTableHeaders)
      .children()
      .each(($elm, i) => {
        expect($elm.text()).equal(tableHeadersCities[i])
      })

    cy.get(selector.customerProfile.list.geoDrawerTableCity)
      .find(selector.customerProfile.list.geoDrawerTableItems)
      .children()
      .its("length")
      .should("be.gt", 0)

    cy.get(selector.engagement.exitDrawer).click()

    // should be able to check if valid response for total customers has received"
    cy.get(selector.customerProfile.chart).its("length").should("gt", 0)

    // should be able to hover over state"
    cy.get(".geochart")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // map state list should have a list of states"
    cy.get(selector.customerProfile.mapStateList)
      .its("length")
      .should("be.gt", 0)

    // should be able to view top location & income chart"
    // validate top location & income chart
    cy.get(selector.customerProfile.incomeChart).its("length").should("gt", 0)

    // should be able to hover over bar of top location & income chart"
    // mouse hover on income chart
    cy.get(".bar")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // should be able to view Gender / monthly spending chart"
    cy.get(selector.customerProfile.genderSpendChart)
      .its("length")
      .should("gt", 0)

    // should be able to view Gender chart"
    cy.get(selector.customerProfile.genderChart).its("length").should("gt", 0)

    // should be able to hover over arc of gender chart"
    cy.get(".arc")
      .first()
      .trigger("mouseover", { force: true, eventConstructor: "MouseEvent" })
  })
})
